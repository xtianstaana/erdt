# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0004_recommendation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': b'Application Period',
                'verbose_name_plural': b'Application Periods',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='erdtform',
            name='application_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to='applicationforms.ApplicationPeriod', unique=True, verbose_name=b'Application Period'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recommendationform',
            name='application_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to='applicationforms.ApplicationPeriod', unique=True, verbose_name=b'Application Period'),
            preserve_default=True,
        ),
    ]
