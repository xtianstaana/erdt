# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0013_auto_20151114_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendationform',
            name='professor_name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
