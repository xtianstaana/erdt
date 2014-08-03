# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0007_purchased_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Research_Dissemination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scholarship', models.ForeignKey(to_field='id', blank=True, to='profiling.Scholarship', null=True)),
                ('paper_title', models.CharField(max_length=100)),
                ('conference_name', models.CharField(max_length=100)),
                ('conference_loc', models.CharField(max_length=100)),
                ('conference_date', models.DateField()),
            ],
            options={
                'verbose_name': b'Research Dissemination',
                'verbose_name_plural': b'Research Disseminations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('university', models.ForeignKey(to='profiling.University', to_field='id')),
                ('course_code', models.CharField(max_length=20)),
                ('course_title', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=250, blank=True)),
                ('course_units', models.FloatField(default=3.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
