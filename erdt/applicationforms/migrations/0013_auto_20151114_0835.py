# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0012_auto_20151114_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationform',
            name='sent_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Sent by', to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='recommendationform',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Created by', to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
