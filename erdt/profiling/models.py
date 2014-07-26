from django.db import models

# Create your models here.

class Person(models.Model):
	MALE, FEMALE = 'M', 'F'
	SEX_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	SINGLE, MARRIED = 'S', 'M'
	CIVIL_STATUS_CHOICES = (
		(SINGLE, 'Single'),
		(MARRIED, 'Married'),
	)

	photo = models.ImageField(upload_to='img', null=True, blank=True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	birthdate = models.DateField()
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)
	civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, default=SINGLE)
	address = models.CharField(max_length=100)
	email_address = models.EmailField()
	landline_number = models.CharField(max_length=20, blank=True)
	mobile_number = models.CharField(max_length=20, blank=True)

	def __unicode__(self):
		return '%s, %s %s' % (self.last_name, self.first_name, self.middle_name)

class University(models.Model):
	photo = models.ImageField(upload_to='univ_seal', null=True, blank=True)
	name = models.CharField(max_length=50)
	member_since = models.DateField()
	address = models.CharField(max_length=100)
	email_address = models.EmailField()
	landline_number = models.CharField(max_length=20, blank=True)
	no_semester = models.IntegerField(default=2, verbose_name='No of terms per SY')
	with_summer = models.BooleanField(default=False, verbose_name='With summer term')

	class Meta:
		verbose_name_plural = 'Universities'

	def __unicode__(self):
		return self.name

class Department(models.Model):
	photo = models.ImageField(upload_to='dept_seal', null=True, blank=True)
	name = models.CharField(max_length=50)
	email_address = models.EmailField()
	landline_number = models.CharField(max_length=20, blank=True)
	university = models.ForeignKey(University)

	def __unicode__(self):
		return '%s, %s' % (self.name, self.university)

class Degree_Program(models.Model):
	MS, PHD = 'MS', 'PHD'
	DEGREE_CHOICES = (
		(MS, 'Master of Science'),
		(PHD, 'Doctor of Philosophy'),
	)

	degree = models.CharField(max_length=3, choices=DEGREE_CHOICES)
	program = models.CharField(max_length=50)
	department = models.ForeignKey(Department)

	class Meta:
		verbose_name = 'Degree Program'
		verbose_name_plural = 'Degree Programs'

	def __unicode__(self):
		return '%s %s' % (self.degree, self.program)

class Scholarship(models.Model):
	ERDT, DOST, AASTHRD = 'ERDT', 'DOST', 'AASTHRD'
	SCHOLARSHIP_TYPE_CHOICES = (
		(ERDT, 'ERDT'),
		(DOST, 'DOST'),
		(AASTHRD, 'AASTHRD'),
	)

	AB, MA, BS, MS, MD, PHD =  'AB', 'MA', 'BS', 'MS', 'MD','PHD'
	DEGREE_CHOICES = (
		(AB, 'Bachelor of Arts'),
		(MA, 'Master of Arts'),
		(BS, 'Bachelor of Science'),
		(MS, 'Master of Science'),
		(MD, 'Doctor of Medicine'),
		(PHD, 'Doctor of Philosophy'),
	)

	PROPOSAL, TOPIC_FINALIZED, PROP_APPROVED, DEFENDED, QUALS, CANDS =  'PR', 'TF', 'PA', 'DF', 'QE', 'CE'
	THESIS_STATUS_CHOICES = (
		(PROPOSAL, 'Proposal'),
		(TOPIC_FINALIZED, 'Topic Finalized'),
		(PROP_APPROVED, 'Proposal Approved'),
		(DEFENDED, 'Defended'),
		(QUALS, 'Qualifying Exam'),
		(CANDS, 'Candidacy Exam'),
	)

	REG_ONGOING, REG_LOAD, ON_EXT, MONITORING, SUSPENDED, TERMINATED, GRADUATE = 'ONG', 'LOAD', 'EXT', 'MON', 'SUS', 'TERM', 'GRAD'
	SCHOLARSHIP_STATUS_CHOICES = (
		(REG_ONGOING, 'Regular - Ongoing'),
		(REG_LOAD, 'Regular - Load'),
		(ON_EXT, 'On Extension'),
		(MONITORING, 'For Monitoring'),
		(SUSPENDED, 'Suspended'),
		(TERMINATED, 'Terminated'),
		(GRADUATE, 'Graduate'),
	)

	adviser = models.ForeignKey(Person)
	degree_program = models.ForeignKey(Degree_Program)
	scholarship_type = models.CharField(max_length=10, choices=SCHOLARSHIP_TYPE_CHOICES, default=ERDT)
	scholarship_status = models.CharField(max_length=3, choices=SCHOLARSHIP_STATUS_CHOICES, default=REG_ONGOING)
	scholarship_detail = models.CharField(max_length=250, blank=True)
	high_degree = models.CharField(max_length=3, choices=DEGREE_CHOICES, default=BS, verbose_name='Highest degree')
	high_degree_univ = models.CharField(max_length=50, verbose_name="Highest degree's University")
	thesis_topic = models.CharField(max_length=100, blank=True)
	thesis_title = models.CharField(max_length=100, blank=True)
	thesis_status = models.CharField(max_length=2, choices=THESIS_STATUS_CHOICES, default=PROPOSAL)
	ce_schedule = models.DateField(null=True, blank=True, verbose_name='Candidacy Exam schedule')
	entry_grad_program = models.DateField(verbose_name='Entry to graduate program')
	entry_scho_program = models.DateField(verbose_name='Start of scholarship contract')
	end_scho_program = models.DateField(verbose_name='End of scholarship contract')
	lateral = models.BooleanField(default=False)

class Profile(models.Model):
	STUDENT, ADVISER, UNIV_ADMIN, CENTRAL_OFFICE, DOST = 'STU', 'ADV', 'ADMIN', 'CENT', 'DOST'
	ROLE_CHOICES = (
		(STUDENT, 'Student'),
		(ADVISER, 'Faculty Adviser'),
		(UNIV_ADMIN, 'Consortium Administrator'),
		(CENTRAL_OFFICE, 'ERDT Central Office'),
		(DOST, 'DOST Office'),
	)

	role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=STUDENT)
	person = models.ForeignKey(Person, null=False, blank=False) # for ALL, account holder
	
	university = models.ForeignKey(University, null=True, blank=True) # for ADMIN, else null
	department = models.ForeignKey(Department, null=True, blank=True) # from ADV, else null
	scholarship = models.ForeignKey(Scholarship,null=True, blank=True) # for STU, else null

	def __unicode__(self):
		return '%s as %s' % (self.person, self.role)

class Purchased_Item(models.Model):
	description = models.CharField(max_length=250)
	location = models.CharField(max_length=100)
	property_no =  models.CharField(max_length=30)
	status = models.CharField(max_length=50)
	accountable = models.ForeignKey(Person)
	fund_source = models.ForeignKey(Scholarship)

	class Meta:
		verbose_name = 'Purchased Item'
		verbose_name_plural = 'Purchased Items'
	
class Research_Dissemination(models.Model):
	profile = models.ForeignKey(Profile)
	paper_title = models.CharField(max_length=100)
	conference_name = models.CharField(max_length=100)
	conference_loc = models.CharField(max_length=100)
	conference_date = models.DateField()

	class Meta:
		verbose_name = 'Research Dissemination'
		verbose_name_plural = 'Research Disseminations'

class Sandwich_Program(models.Model):
	budget = models.FloatField(default=0.0)
	host_university = models.CharField(max_length=50)
	host_professor = models.CharField(max_length=50)
	scholarship = models.ForeignKey(Scholarship)

	class Meta:
		verbose_name = 'Sandwich Program'
		verbose_name_plural = 'Sandwich Programs'

class Subject(models.Model):
	university = models.ForeignKey(University)
	course_title = models.CharField(max_length=100)
	course_units = models.FloatField(default=3.0)

	def __unicode__(self):
		return '%s: %s' % (self.course_title, self.university)

class Enrolled_Subject(models.Model):
	subject = models.ForeignKey(Subject)
	scholarship = models.ForeignKey(Scholarship)
	year_taken = models.DateField()
	sem_taken = models.IntegerField(default=1)
	eq_grade = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Enrolled Subject'
		verbose_name_plural = 'Enrolled Subjects'

