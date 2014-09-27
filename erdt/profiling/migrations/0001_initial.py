# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree_Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=3, choices=[(b'MS', b'Master of Science'), (b'PHD', b'Doctor of Philosophy')])),
                ('program', models.CharField(max_length=100)),
                ('no_semester', models.IntegerField(default=6, verbose_name=b'No of semester including summer')),
            ],
            options={
                'verbose_name': b'Degree Program',
                'verbose_name_plural': b'Degree Programs',
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='degree_program',
            name='department',
            field=models.ForeignKey(to='profiling.Department'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Enrolled_Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('landline_number', models.CharField(max_length=100, blank=True)),
                ('mobile_number', models.CharField(max_length=100, blank=True)),
                ('user', models.OneToOneField(verbose_name=b'User account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'STU', max_length=5, choices=[(b'STU', b'Student'), (b'ADV', b'Faculty Adviser'), (b'ADMIN', b'Consortium Administrator'), (b'CENT', b'ERDT Central Office'), (b'DOST', b'DOST Office')])),
                ('active', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='profiling.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchased_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100)),
                ('property_no', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=50)),
                ('consumable', models.BooleanField(default=False)),
                ('date_procured', models.DateField()),
                ('accountable', models.ForeignKey(to='profiling.Person')),
                ('issuance', models.ForeignKey(verbose_name=b'Issued to', to='profiling.Person')),
                ('item_tag', models.ManyToManyField(to='profiling.Item_Tag')),
            ],
            options={
                'verbose_name': b'Purchased Item',
                'verbose_name_plural': b'Purchased Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Research_Dissemination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
        migrations.CreateModel(
            name='Sandwich_Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('budget', models.FloatField(default=0.0)),
                ('host_university', models.CharField(max_length=50)),
                ('host_professor', models.CharField(max_length=50)),
                ('person', models.ForeignKey(to='profiling.Person')),
            ],
            options={
                'verbose_name': b'Sandwich Program',
                'verbose_name_plural': b'Sandwich Programs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scholarship_type', models.CharField(default=b'ERDT', max_length=10, choices=[(b'ERDT', b'ERDT'), (b'DOST', b'DOST'), (b'AASTHRD', b'AASTHRD')])),
                ('scholarship_status', models.CharField(default=b'ONG', max_length=3, choices=[(b'ONG', b'Regular - Ongoing'), (b'LOAD', b'Regular - Load'), (b'EXT', b'On Extension'), (b'MON', b'For Monitoring'), (b'SUS', b'Suspended'), (b'TERM', b'Terminated'), (b'GRAD', b'Graduate')])),
                ('scholarship_detail', models.CharField(max_length=250, blank=True)),
                ('high_degree', models.CharField(default=b'BS', max_length=3, verbose_name=b'Highest degree', choices=[(b'AB', b'Bachelor of Arts'), (b'MA', b'Master of Arts'), (b'BS', b'Bachelor of Science'), (b'MS', b'Master of Science'), (b'MD', b'Doctor of Medicine'), (b'PHD', b'Doctor of Philosophy')])),
                ('thesis_topic', models.CharField(max_length=100, blank=True)),
                ('thesis_title', models.CharField(max_length=100, blank=True)),
                ('thesis_status', models.CharField(default=b'PR', max_length=2, choices=[(b'PR', b'Proposal Stage'), (b'TF', b'Topic Finalized'), (b'PA', b'Proposal Approved'), (b'DF', b'Defended'), (b'QE', b'Qualifying Exam'), (b'CE', b'Candidacy Exam')])),
                ('ce_schedule', models.DateField(null=True, verbose_name=b'Candidacy Exam schedule', blank=True)),
                ('entry_grad_program', models.DateField(verbose_name=b'Entry to graduate program')),
                ('entry_scho_program', models.DateField(verbose_name=b'Start of scholarship contract')),
                ('end_scho_program', models.DateField(verbose_name=b'End of scholarship contract')),
                ('lateral', models.BooleanField(default=False)),
                ('adviser', models.ForeignKey(to='profiling.Person')),
                ('degree_program', models.ForeignKey(to='profiling.Degree_Program')),
                ('scholar', models.ForeignKey(to='profiling.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='research_dissemination',
            name='scholarship',
            field=models.ForeignKey(blank=True, to='profiling.Scholarship', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchased_item',
            name='fund_source',
            field=models.ManyToManyField(to='profiling.Scholarship', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrolled_subject',
            name='scholarship',
            field=models.ForeignKey(to='profiling.Scholarship'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(max_length=20)),
                ('course_title', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=250, blank=True)),
                ('course_units', models.FloatField(default=3.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='enrolled_subject',
            name='subject',
            field=models.ForeignKey(to='profiling.Subject'),
            preserve_default=True,
        ),
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
        migrations.AddField(
            model_name='subject',
            name='university',
            field=models.ForeignKey(to='profiling.University'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scholarship',
            name='high_degree_univ',
            field=models.ForeignKey(verbose_name=b"Highest degree's University", to='profiling.University'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='university',
            field=models.ForeignKey(blank=True, to='profiling.University', help_text=b'Leave blank for DOST or ERDT Central Office role.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='department',
            name='university',
            field=models.ForeignKey(to='profiling.University'),
            preserve_default=True,
        ),
    ]
