# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0008_enrolled_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='account',
            new_name='user',
        ),
    ]
