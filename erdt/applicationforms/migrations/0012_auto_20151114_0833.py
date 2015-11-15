# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0011_recommendationform_recommendation_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationform',
            name='application_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Application Period', to_field='id', blank=True, to='applicationforms.ApplicationPeriod', null=True),
        ),
    ]
