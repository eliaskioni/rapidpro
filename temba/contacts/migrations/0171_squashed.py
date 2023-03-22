# Generated by Django 4.0.8 on 2023-01-11 15:35

import django.db.models.deletion
import django.db.models.expressions
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contacts", "0170_squashed"),
        ("flows", "0314_squashed"),
        ("orgs", "0118_squashed"),
        ("channels", "0158_squashed"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="exportcontactstask",
            name="org",
            field=models.ForeignKey(
                help_text="The organization of the user.",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)ss",
                to="orgs.org",
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="channel",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="urns", to="channels.channel"
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="contact",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="urns", to="contacts.contact"
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="org",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="urns", to="orgs.org"),
        ),
        migrations.AddField(
            model_name="contactimportbatch",
            name="contact_import",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="batches", to="contacts.contactimport"
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="imports",
                to="contacts.contactgroup",
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="contact_imports", to="orgs.org"
            ),
        ),
        migrations.AddField(
            model_name="contactgroupcount",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="counts", to="contacts.contactgroup"
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="contacts",
            field=models.ManyToManyField(related_name="groups", to="contacts.contact"),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="org",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="groups", to="orgs.org"),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="query_fields",
            field=models.ManyToManyField(related_name="dependent_groups", to="contacts.contactfield"),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="org",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="fields", to="orgs.org"),
        ),
        migrations.AddField(
            model_name="contact",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="current_flow",
            field=models.ForeignKey(
                db_index=False, null=True, on_delete=django.db.models.deletion.PROTECT, to="flows.flow"
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="modified_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="contacts", to="orgs.org"
            ),
        ),
        migrations.AddConstraint(
            model_name="contacturn",
            constraint=models.CheckConstraint(
                check=models.Q(models.Q(("scheme", ""), ("path", ""), _connector="OR"), _negated=True),
                name="non_empty_scheme_and_path",
            ),
        ),
        migrations.AddConstraint(
            model_name="contacturn",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "identity",
                        django.db.models.functions.text.Concat(
                            django.db.models.expressions.F("scheme"),
                            django.db.models.expressions.Value(":"),
                            django.db.models.expressions.F("path"),
                        ),
                    )
                ),
                name="identity_matches_scheme_and_path",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="contacturn",
            unique_together={("identity", "org")},
        ),
        migrations.AddConstraint(
            model_name="contactgroup",
            constraint=models.UniqueConstraint(
                django.db.models.expressions.F("org"),
                django.db.models.functions.text.Lower("name"),
                name="unique_contact_group_names",
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(fields=["org", "-modified_on"], name="contacts_contact_org_modified"),
        ),
    ]