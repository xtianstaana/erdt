# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree_Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=3, choices=[(b'MS', b'Master of Science'), (b'PHD', b'Doctor of Philosophy')])),
                ('program', models.CharField(max_length=100)),
                ('no_semester', models.IntegerField(default=6, verbose_name=b'No of semester including summer')),
                ('department', models.ForeignKey(to='profiling.Department', to_field='id')),
            ],
            options={
                'verbose_name': b'Degree Program',
                'verbose_name_plural': b'Degree Programs',
            },
            bases=(models.Model,),
        ),
    ]
