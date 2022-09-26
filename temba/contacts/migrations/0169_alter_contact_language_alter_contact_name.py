# Generated by Django 4.0.7 on 2022-09-23 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0168_alter_exportcontactstask_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="language",
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name="Language"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="name",
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name="Name"),
        ),
    ]
