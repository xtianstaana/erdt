# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiling', '0003_scholarship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'STU', max_length=5, choices=[(b'STU', b'Student'), (b'ADV', b'Faculty Adviser'), (b'ADMIN', b'Consortium Administrator'), (b'CENT', b'ERDT Central Office'), (b'DOST', b'DOST Office')])),
                ('person', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('university', models.ForeignKey(to_field='id', blank=True, to='profiling.University', null=True)),
                ('department', models.ForeignKey(to_field='id', blank=True, to='profiling.Department', null=True)),
                ('scholarship', models.ForeignKey(to_field='id', blank=True, to='profiling.Scholarship', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
