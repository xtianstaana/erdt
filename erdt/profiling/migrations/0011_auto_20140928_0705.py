# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0010_profile_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='scholarship_status',
            field=models.CharField(default=b'ONG', max_length=5, choices=[(b'ONG', b'Regular - Ongoing'), (b'LOAD', b'Regular - Load'), (b'EXT', b'On Extension'), (b'MON', b'For Monitoring'), (b'SUS', b'Suspended'), (b'TERM', b'Terminated'), (b'GRAD', b'Graduate')]),
        ),
    ]
