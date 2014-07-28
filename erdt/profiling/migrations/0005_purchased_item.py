# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0004_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchased_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100)),
                ('property_no', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=50)),
                ('accountable', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('fund_source', models.ForeignKey(to='profiling.Scholarship', to_field='id')),
            ],
            options={
                'verbose_name': b'Purchased Item',
                'verbose_name_plural': b'Purchased Items',
            },
            bases=(models.Model,),
        ),
    ]
