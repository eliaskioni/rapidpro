from django.utils.translation import gettext_lazy as _

from temba.channels.types.jasmin.views import ClaimView
from temba.contacts.models import URN

from ...models import ChannelType, ConfigUI


class JasminType(ChannelType):
    """
    An Jasmin channel (http://www.jasminsms.com/)
    """

    code = "JS"
    category = ChannelType.Category.PHONE

    courier_url = r"^js/(?P<uuid>[a-z0-9\-]+)/(?P<action>status|receive)$"

    name = "Jasmin"

    claim_blurb = _("Connect your %(link)s instance that you have already connected to an SMSC.") % {
        "link": '<a target="_blank" href="http://www.jasminsms.com/">Jasmin</a>'
    }
    claim_view = ClaimView

    schemes = [URN.TEL_SCHEME]
    max_length = 1600

    config_ui = ConfigUI(
        blurb=_("As a last step you'll need to configure Jasmin to call the following URL for MO (incoming) messages."),
        endpoints=[
            ConfigUI.Endpoint(
                courier="receive",
                label=_("Push Message URL"),
                help=_(
                    "This endpoint will be called by Jasmin when new messages are received to your number, "
                    "it must be configured to be called as a POST."
                ),
            ),
        ],
    )
