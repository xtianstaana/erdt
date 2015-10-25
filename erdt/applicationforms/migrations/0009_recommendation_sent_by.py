# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicationforms', '0008_recommendation_sent_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='sent_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to=settings.AUTH_USER_MODEL, unique=True, verbose_name=b'Sent by'),
            preserve_default=True,
        ),
    ]
