# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0006_research_dissemination'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sandwich_Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('budget', models.FloatField(default=0.0)),
                ('host_university', models.CharField(max_length=50)),
                ('host_professor', models.CharField(max_length=50)),
                ('scholarship', models.ForeignKey(to='profiling.Scholarship', to_field='id')),
            ],
            options={
                'verbose_name': b'Sandwich Program',
                'verbose_name_plural': b'Sandwich Programs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('university', models.ForeignKey(to='profiling.University', to_field='id')),
                ('course_title', models.CharField(max_length=100)),
                ('course_units', models.FloatField(default=3.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
