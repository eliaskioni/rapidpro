# This is a dummy migration which will be implemented in the next release

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("classifiers", "0012_squashed"),
        ("orgs", "0133_squashed"),
    ]

    operations = []
