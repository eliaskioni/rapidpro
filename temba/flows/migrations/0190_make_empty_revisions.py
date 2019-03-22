# Generated by Django 2.1.3 on 2018-12-11 15:22

from django.db import migrations


def create_revisions(apps, schema_editor):
    Flow = apps.get_model("flows", "Flow")

    # for each flow without a revision
    for flow in Flow.objects.filter(is_active=True, revisions=None):
        print(f"Creating revision for: {flow.name}")

        # sanity check there we're not blowing away something that has nodes but no revisions
        if flow.action_sets.exists() or flow.rule_sets.exists():
            raise ValueError("flow has rulesets/actionsets but no revisions")

        definition = {
            "flow_type": flow.flow_type,
            "version": "11.12",
            "base_language": flow.base_language,
            "action_sets": [],
            "rule_sets": [],
            "metadata": {
                "uuid": str(flow.uuid),
                "name": flow.name,
                "revision": 1,
                "expires": flow.expires_after_minutes,
            },
        }

        flow.revisions.create(definition=definition, revision=1, spec_version="11.12")


class Migration(migrations.Migration):

    dependencies = [("flows", "0189_flowsession_wait_started_on")]

    operations = [migrations.RunPython(create_revisions)]
