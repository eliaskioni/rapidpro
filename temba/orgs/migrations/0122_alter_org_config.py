# Generated by Django 4.1.7 on 2023-03-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("orgs", "0121_alter_org_config")]

    operations = [
        migrations.AlterField(model_name="org", name="config", field=models.JSONField(default=dict)),
    ]
