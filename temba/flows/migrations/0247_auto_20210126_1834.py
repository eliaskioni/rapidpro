# Generated by Django 2.2.10 on 2021-01-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flows", "0246_auto_20210119_1717"),
        ("sql", "0002_squashed"),
    ]

    operations = [
        migrations.RunSQL("DROP FUNCTION temba_flow_for_run(_run_id INT);"),
        migrations.AlterField(
            model_name="flowpathrecentrun", name="id", field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
