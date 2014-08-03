# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0004_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sandwich_Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('budget', models.FloatField(default=0.0)),
                ('host_university', models.CharField(max_length=50)),
                ('host_professor', models.CharField(max_length=50)),
                ('person', models.ForeignKey(to='profiling.Person', to_field='id')),
            ],
            options={
                'verbose_name': b'Sandwich Program',
                'verbose_name_plural': b'Sandwich Programs',
            },
            bases=(models.Model,),
        ),
    ]
