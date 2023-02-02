from unittest.mock import patch

from twilio.base.exceptions import TwilioRestException

from django.urls import reverse

from temba.channels.models import Channel
from temba.orgs.models import Org
from temba.tests import TembaTest
from temba.tests.twilio import MockRequestValidator, MockTwilioClient

from .type import TwilioMessagingServiceType
from .views import COUNTRY_CHOICES


class TwilioMessagingServiceTypeTest(TembaTest):
    @patch("temba.orgs.models.TwilioClient", MockTwilioClient)
    @patch("twilio.request_validator.RequestValidator", MockRequestValidator)
    def test_claim(self):

        self.login(self.admin)

        claim_twilio_ms = reverse("channels.types.twilio_messaging_service.claim")

        # remove any existing channels
        self.org.channels.all().delete()

        # make sure twilio is on the claim page
        response = self.client.get(reverse("channels.channel_claim"))
        self.assertContains(response, "Twilio")

        response = self.client.get(claim_twilio_ms)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(claim_twilio_ms, follow=True)
        self.assertEqual(response.request["PATH_INFO"], reverse("orgs.org_twilio_connect"))

        twilio_config = dict()
        twilio_config[Org.CONFIG_TWILIO_SID] = "account-sid"
        twilio_config[Org.CONFIG_TWILIO_TOKEN] = "account-token"

        self.org.config = twilio_config
        self.org.save()

        response = self.client.get(reverse("channels.channel_claim"))
        self.assertContains(response, claim_twilio_ms)

        response = self.client.get(claim_twilio_ms)
        self.assertIn("account_trial", response.context)
        self.assertFalse(response.context["account_trial"])

        with patch("temba.orgs.models.Org.get_twilio_client") as mock_get_twilio_client:
            mock_get_twilio_client.return_value = None

            response = self.client.get(claim_twilio_ms)
            self.assertRedirects(response, f'{reverse("orgs.org_twilio_connect")}?claim_type=twilio_messaging_service')

            mock_get_twilio_client.side_effect = TwilioRestException(
                401, "http://twilio", msg="Authentication Failure", code=20003
            )

            response = self.client.get(claim_twilio_ms)
            self.assertRedirects(response, f'{reverse("orgs.org_twilio_connect")}?claim_type=twilio_messaging_service')

        with patch("temba.tests.twilio.MockTwilioClient.MockAccounts.get") as mock_get:
            mock_get.return_value = MockTwilioClient.MockAccount("Trial")

            response = self.client.get(claim_twilio_ms)
            self.assertIn("account_trial", response.context)
            self.assertTrue(response.context["account_trial"])

        response = self.client.get(claim_twilio_ms)
        self.assertEqual(response.context["form"].fields["country"].choices, list(COUNTRY_CHOICES))

        response = self.client.post(claim_twilio_ms, dict())
        self.assertTrue(response.context["form"].errors)

        response = self.client.post(claim_twilio_ms, dict(country="US", messaging_service_sid="MSG-SERVICE-SID"))
        channel = self.org.channels.get()
        self.assertRedirects(response, reverse("channels.channel_configuration", args=[channel.uuid]))
        self.assertEqual(channel.channel_type, "TMS")

        channel_config = channel.config
        self.assertEqual(channel_config["messaging_service_sid"], "MSG-SERVICE-SID")
        self.assertTrue(channel_config["account_sid"])
        self.assertTrue(channel_config["auth_token"])

        response = self.client.get(reverse("channels.channel_configuration", args=[channel.uuid]))
        self.assertContains(response, reverse("courier.tms", args=[channel.uuid, "receive"]))

    def test_get_error_ref_url(self):
        self.assertEqual(
            "https://www.twilio.com/docs/api/errors/30006",
            TwilioMessagingServiceType().get_error_ref_url(None, "30006"),
        )

    @patch("temba.channels.types.twilio.views.TwilioClient", MockTwilioClient)
    @patch("temba.channels.types.twilio.type.TwilioClient", MockTwilioClient)
    @patch("twilio.request_validator.RequestValidator", MockRequestValidator)
    def test_update(self):
        self.org.connect_twilio("TEST_SID", "TEST_TOKEN", self.admin)
        tms_channel = self.org.channels.all().first()
        tms_channel.channel_type = "TMS"
        tms_channel.save()

        update_url = reverse("channels.channel_update", args=[tms_channel.id])

        self.login(self.admin)
        response = self.client.get(update_url)
        self.assertEqual(
            ["name", "allow_international", "account_sid", "auth_token", "loc"],
            list(response.context["form"].fields.keys()),
        )

        post_data = dict(name="Foo channel", allow_international=False, account_sid="ACC_SID", auth_token="ACC_Token")

        response = self.client.post(update_url, post_data)

        self.assertEqual(response.status_code, 302)

        tms_channel.refresh_from_db()
        self.assertEqual(tms_channel.name, "Foo channel")
        # we used the primary credentials returned on the account fetch even though we submit the others
        self.assertEqual(tms_channel.config[Channel.CONFIG_ACCOUNT_SID], "AccountSid")
        self.assertEqual(tms_channel.config[Channel.CONFIG_AUTH_TOKEN], "AccountToken")
        self.assertTrue(tms_channel.check_credentials())

        with patch(
            "temba.channels.types.twilio_messaging_service.type.TwilioMessagingServiceType.check_credentials"
        ) as mock_check_credentials:
            mock_check_credentials.return_value = False

            response = self.client.post(update_url, post_data)
            self.assertFormError(response, "form", "__all__", "Channel credentials don't appear to be valid.")
