# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0005_purchased_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Research_Dissemination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile', models.ForeignKey(to='profiling.Profile', to_field='id')),
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
    ]
