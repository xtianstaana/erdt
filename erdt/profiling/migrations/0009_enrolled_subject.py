# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0008_research_dissemination_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolled_Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.ForeignKey(to='profiling.Subject', to_field='id')),
                ('scholarship', models.ForeignKey(to='profiling.Scholarship', to_field='id')),
                ('year_taken', models.DateField()),
                ('sem_taken', models.IntegerField(default=1, verbose_name=b'Semester taken')),
                ('eq_grade', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': b'Enrolled Subject',
                'verbose_name_plural': b'Enrolled Subjects',
            },
            bases=(models.Model,),
        ),
    ]
