# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0014_recommendationform_professor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erdtform',
            name='application_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Application Period', to_field='id', blank=True, to='applicationforms.ApplicationPeriod', null=True),
        ),
        migrations.AlterField(
            model_name='erdtform',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Created by', to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
