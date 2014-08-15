# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'univ_seal', blank=True)),
                ('name', models.CharField(max_length=50)),
                ('is_consortium', models.BooleanField(default=False)),
                ('member_since', models.DateField(null=True, blank=True)),
                ('address', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=100, blank=True)),
                ('no_semester', models.IntegerField(default=2, verbose_name=b'No of semester per SY')),
                ('with_summer', models.BooleanField(default=False, verbose_name=b'With summer semester')),
            ],
            options={
                'verbose_name_plural': b'Universities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item_Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'verbose_name': b'Item Tag',
                'verbose_name_plural': b'Item Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'dept_seal', blank=True)),
                ('name', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=100, blank=True)),
                ('university', models.ForeignKey(to='profiling.University', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
