# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0005_sandwich_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adviser', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('scholar', models.ForeignKey(to='profiling.Person', to_field='id')),
                ('degree_program', models.ForeignKey(to='profiling.Degree_Program', to_field='id')),
                ('scholarship_type', models.CharField(default=b'ERDT', max_length=10, choices=[(b'ERDT', b'ERDT'), (b'DOST', b'DOST'), (b'AASTHRD', b'AASTHRD')])),
                ('scholarship_status', models.CharField(default=b'ONG', max_length=3, choices=[(b'ONG', b'Regular - Ongoing'), (b'LOAD', b'Regular - Load'), (b'EXT', b'On Extension'), (b'MON', b'For Monitoring'), (b'SUS', b'Suspended'), (b'TERM', b'Terminated'), (b'GRAD', b'Graduate')])),
                ('scholarship_detail', models.CharField(max_length=250, blank=True)),
                ('high_degree', models.CharField(default=b'BS', max_length=3, verbose_name=b'Highest degree', choices=[(b'AB', b'Bachelor of Arts'), (b'MA', b'Master of Arts'), (b'BS', b'Bachelor of Science'), (b'MS', b'Master of Science'), (b'MD', b'Doctor of Medicine'), (b'PHD', b'Doctor of Philosophy')])),
                ('high_degree_univ', models.ForeignKey(to='profiling.University', to_field='id', verbose_name=b"Highest degree's University")),
                ('thesis_topic', models.CharField(max_length=100, blank=True)),
                ('thesis_title', models.CharField(max_length=100, blank=True)),
                ('thesis_status', models.CharField(default=b'PR', max_length=2, choices=[(b'PR', b'Proposal Stage'), (b'TF', b'Topic Finalized'), (b'PA', b'Proposal Approved'), (b'DF', b'Defended'), (b'QE', b'Qualifying Exam'), (b'CE', b'Candidacy Exam')])),
                ('ce_schedule', models.DateField(null=True, verbose_name=b'Candidacy Exam schedule', blank=True)),
                ('entry_grad_program', models.DateField(verbose_name=b'Entry to graduate program')),
                ('entry_scho_program', models.DateField(verbose_name=b'Start of scholarship contract')),
                ('end_scho_program', models.DateField(verbose_name=b'End of scholarship contract')),
                ('lateral', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
