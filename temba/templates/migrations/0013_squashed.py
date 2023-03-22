# Generated by Django 4.0.8 on 2023-01-11 15:35

import uuid

import django_countries.fields

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("channels", "0157_squashed"),
        ("orgs", "0118_squashed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Template",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("name", models.CharField(max_length=512)),
                ("modified_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="templates", to="orgs.org"
                    ),
                ),
            ],
            options={
                "unique_together": {("org", "name")},
            },
        ),
        migrations.CreateModel(
            name="TemplateTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField()),
                ("variable_count", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "approved"),
                            ("P", "pending"),
                            ("R", "rejected"),
                            ("U", "unsupported_language"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("language", models.CharField(max_length=6)),
                ("country", django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ("namespace", models.CharField(default="", max_length=36)),
                ("external_id", models.CharField(max_length=64, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="template_translations",
                        to="channels.channel",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="translations",
                        to="templates.template",
                    ),
                ),
            ],
        ),
    ]