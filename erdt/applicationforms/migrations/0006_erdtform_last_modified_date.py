# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0005_auto_20151025_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='erdtform',
            name='last_modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 12, 8, 47, 993644)),
            preserve_default=False,
        ),
    ]
