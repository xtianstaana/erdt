# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicationforms', '0002_erdtform'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendationForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.ForeignKey(to='applicationforms.Token', to_field='id')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to=settings.AUTH_USER_MODEL, unique=True, verbose_name=b'Created by')),
                ('created_date', models.DateTimeField()),
                ('status', models.CharField(max_length=100, choices=[(b'In Progress', b'In Progress'), (b'Submitted', b'Submitted')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
