# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiling', '0002_degree_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(verbose_name=b'User account', to_field='id', to=settings.AUTH_USER_MODEL)),
                ('photo', models.ImageField(null=True, upload_to=b'img', blank=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birthdate', models.DateField()),
                ('sex', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('civil_status', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Single'), (b'M', b'Married')])),
                ('address', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=75)),
                ('landline_number', models.CharField(max_length=100, blank=True)),
                ('mobile_number', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
