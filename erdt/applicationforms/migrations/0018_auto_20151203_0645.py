# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0017_auto_20151118_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationform',
            name='created_by',
            field=models.ForeignKey(related_name='recommendationforms_created', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendationform',
            name='sent_by',
            field=models.ForeignKey(related_name='recommendationforms_sent', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Sent by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
