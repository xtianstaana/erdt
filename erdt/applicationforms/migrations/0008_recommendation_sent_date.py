# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0007_recommendation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='sent_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 12, 28, 17, 416537)),
            preserve_default=False,
        ),
    ]
