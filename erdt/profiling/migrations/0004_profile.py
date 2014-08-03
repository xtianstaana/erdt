# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0003_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'STU', max_length=5, choices=[(b'STU', b'Student'), (b'ADV', b'Faculty Adviser'), (b'ADMIN', b'Consortium Administrator'), (b'CENT', b'ERDT Central Office'), (b'DOST', b'DOST Office')])),
                ('person', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('university', models.ForeignKey(to_field='id', blank=True, to='profiling.University', help_text=b'Leave blank for DOST or ERDT Central Office role.', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
