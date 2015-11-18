# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicationforms', '0015_auto_20151115_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='UPDERDTForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_period', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Application Period', to_field='id', blank=True, to='applicationforms.ApplicationPeriod', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Created by', to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('created_date', models.DateTimeField()),
                ('last_modified_date', models.DateTimeField()),
                ('status', models.CharField(max_length=100, choices=[(b'In Progress', b'In Progress'), (b'Submitted', b'Submitted')])),
                ('scholarship_applied_for', models.CharField(max_length=100, choices=[(b'ME', b'ME'), (b'MS', b'MS'), (b'DE', b'DE'), (b'PhD', b'PhD')])),
                ('program_of_study', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
