# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0010_auto_20151114_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendationform',
            name='recommendation_box',
            field=models.CharField(default='', max_length=500, verbose_name=b'Recommendation', blank=True),
            preserve_default=False,
        ),
    ]
