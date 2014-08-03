# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0006_scholarship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchased_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issuance', models.ForeignKey(to='profiling.Person', to_field='id', verbose_name=b'Issued to')),
                ('description', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100)),
                ('property_no', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=50)),
                ('consumable', models.BooleanField(default=False)),
                ('date_procured', models.DateField()),
                ('accountable', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('item_tag', models.ManyToManyField(to='profiling.Item_Tag')),
                ('fund_source', models.ManyToManyField(to='profiling.Scholarship', null=True, blank=True)),
            ],
            options={
                'verbose_name': b'Purchased Item',
                'verbose_name_plural': b'Purchased Items',
            },
            bases=(models.Model,),
        ),
    ]
