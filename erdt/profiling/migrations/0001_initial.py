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
                ('member_since', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=20, blank=True)),
                ('no_semester', models.IntegerField(default=2, verbose_name=b'No of terms per SY')),
                ('with_summer', models.BooleanField(default=False, verbose_name=b'With summer term')),
            ],
            options={
                'verbose_name_plural': b'Universities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'img', blank=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birthdate', models.DateField()),
                ('sex', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('civil_status', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Single'), (b'M', b'Married')])),
                ('address', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=20, blank=True)),
                ('mobile_number', models.CharField(max_length=20, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'dept_seal', blank=True)),
                ('name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=20, blank=True)),
                ('university', models.ForeignKey(to='profiling.University', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
