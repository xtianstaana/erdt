# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicationforms', '0009_recommendation_sent_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendationform',
            name='professor_email',
            field=models.EmailField(default='', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recommendationform',
            name='sent_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to=settings.AUTH_USER_MODEL, unique=True, verbose_name=b'Sent by'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recommendationform',
            name='sent_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 6, 26, 15, 196435)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recommendationform',
            name='status',
            field=models.CharField(max_length=100, choices=[(b'In Progress', b'In Progress'), (b'Submitted', b'Submitted'), (b'Not Started', b'Not Started')]),
        ),
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]
