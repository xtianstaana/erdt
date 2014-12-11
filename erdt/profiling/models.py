from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from polymorphic import PolymorphicModel
from datetime import date
from django.utils.html import format_html

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

	user = models.ForeignKey(User, verbose_name='User account', null=True, blank=True) 
	photo = models.ImageField(upload_to='img', null=True, blank=True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	birthdate = models.DateField()
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)
	civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, default=SINGLE)
	address = models.CharField(max_length=250)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=100, blank=True)
	mobile_number = models.CharField(max_length=100, blank=True)

	def age(self):
		today = date.today()
		return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

	def clean(self):
		if self.landline_number.strip() == '' and self.mobile_number.strip() == '' and self.email_address.strip() == '':
			raise ValidationError('Provide at least one contact number or an email address.')

	def is_adviser(self):
		return self.profile_set.filter(role=Profile.ADVISER, university=self.university).count() > 0

	def __unicode__(self):
		return '%s, %s %s' % (self.last_name, self.first_name, self.middle_name)

class University(models.Model):
	photo = models.ImageField(upload_to='univ_seal', null=True, blank=True)
	name = models.CharField(max_length=150)
	is_consortium = models.BooleanField(default=False, verbose_name='ERDT Consortium')
	member_since = models.DateField(null=True, blank=True) 
	address = models.CharField(max_length=100, blank=True)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=100, blank=True)
	no_semester = models.IntegerField(default=2, null=True, blank=True, verbose_name='No of semester per SY')
	with_summer = models.BooleanField(default=False, verbose_name='With summer semester')

	def clean(self):
		if not self.is_consortium:
			self.member_since = None
		else:
			if not self.member_since:
				raise ValidationError('Specify membership date.')

	class Meta:
		verbose_name_plural = 'Universities'

	def __unicode__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=150)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=50, blank=True)
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})

	def __unicode__(self):
		return '%s, %s' % (self.name, self.university)

	def clean(self):
		if not self.university.is_consortium:
			raise ValidationError('University must be an ERDT consortium member to add departments.')

class Degree_Program(models.Model):
	MS, PHD, ME, DE = 'MS', 'PHD', 'ME', 'DE'
	DEGREE_CHOICES = (
		(MS, 'Master of Science'),
		(PHD, 'Doctor of Philosophy'),
		(ME, 'Master of Engineering'),
		(DE, 'Doctor of Engineering'),
	)

	degree = models.CharField(max_length=5, choices=DEGREE_CHOICES)
	program = models.CharField(max_length=150)
	no_semester = models.IntegerField(default=6, verbose_name='No of semester including summer')
	department = models.ForeignKey(Department)

	class Meta:
		verbose_name = 'Degree Program'
		verbose_name_plural = 'Degree Programs'

	def __unicode__(self):
		return '%s %s, %s' % (self.degree, self.program, self.department.university.__unicode__())

class Subject(models.Model):
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})
	title = models.CharField(max_length=100, verbose_name='Course title')
	code = models.CharField(max_length=20, blank=True, verbose_name='Course code')
	description = models.CharField(max_length=250, blank=True)
	units = models.FloatField(default=3.0)

	def __unicode__(self):
		return '%s: %s' % (self.title, self.university.__unicode__())

	def clean(self):
		if not self.university.is_consortium:
			raise ValidationError('University must be an ERDT consortium member to add subjects.')

class Enrolled_Subject(models.Model):
	subject = models.ForeignKey(Subject)
	scholar = models.ForeignKey(Person)
	year_taken = models.DateField()
	sem_taken = models.IntegerField(default=1, verbose_name='Semester taken')
	eq_grade = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Enrolled Subject'
		verbose_name_plural = 'Enrolled Subjects'

	def __unicode__(self):
		return '%s: %s' % (self.scholar.__unicode__(), self.subject.__unicode__())

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
	person = models.ForeignKey(Person)
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True}, help_text='Leave blank for DOST or ERDT Central Office role.', null=True, blank=True)	
	active = models.BooleanField(default=False)

	class Meta:
		unique_together = ('role', 'person',)

	def __unicode__(self):
		return '%s as %s' % (self.person, self.get_role_display())

	def clean(self):
		if self.role in (self.DOST, self.CENTRAL_OFFICE):
			self.university = None
		elif self.role in (self.STUDENT, self.ADVISER, self.UNIV_ADMIN):
			if self.university == None:
				raise ValidationError('Specify university of affiliation.')

class Grant(PolymorphicModel):
	recipient = models.ForeignKey(Person, related_name='grant_recipient')
	description = models.CharField(max_length=250, blank=True)
	start_date = models.DateField(verbose_name='Start of contract')
	end_date = models.DateField(verbose_name='End of contract')
	total_amount = models.FloatField(default=0.0, verbose_name='Allotment (PhP)')

	class Meta:
		verbose_name = 'Grant'
		verbose_name_plural = 'Grants'

	def grant_type(self):
		return 'Grant'

	def total_released(self):
		total_amount = 0.0
		for rel in Grant_Allocation_Release.objects.filter(grant__id=self.id):
			total_amount = total_amount + rel.amount_released
		return total_amount
	total_released.short_description = 'Released (PhP)'

	def total_liquidated(self):
		total_amount = 0.0
		for rel in Grant_Allocation_Release.objects.filter(grant__id=self.id):
			total_amount = total_amount + rel.amount_liquidated
		return total_amount
	total_liquidated.short_description = 'Liquidated (PhP)'

	def total_remaining(self):
		total_amount = 0.0
		for rel in Grant_Allocation_Release.objects.filter(grant__id=self.id):
			total_amount = total_amount + rel.amount_liquidated	
		return format_html("<b> %s </b>" % str(self.total_amount - total_amount))
	total_remaining.short_description = 'Remaining (PhP)'

	def __unicode__(self):
		return '%s: %s' % (self.grant_type(), self.recipient.__unicode__())

	def clean(self):
		if self.recipient.profile_set.filter(Q(role=Profile.ADVISER)|Q(role=Profile.STUDENT)).count() == 0:
			raise ValidationError('Recipient of grant must have Faculty Adviser or Student profile.')

		if self.start_date == self.end_date:
			raise ValidationError('Start and end of grant dates can not be the same.')

class Grant_Allocation(models.Model):
	grant = models.ForeignKey(Grant)
	name = models.CharField(max_length=150, verbose_name="Line item")
	description = models.CharField(max_length=350, blank=True)
	amount = models.FloatField()

	class Meta:
		verbose_name = 'Grant Allocation'
		verbose_name_plural = 'Grant Allocations'

	def __unicode__(self):
		return '%s: %s' % (self.grant.__unicode__(), self.name)

class Grant_Allocation_Release(PolymorphicModel):
	recipient = models.ForeignKey(Person, related_name='recipient')
	grant = models.ForeignKey(Grant, null=True, blank=True)
	allocation = models.ForeignKey(Grant_Allocation, null=True, blank=True)
	description = models.CharField(max_length=350, blank=True)
	amount_released = models.FloatField(default=0.0, verbose_name='Released (PhP)')
	amount_liquidated = models.FloatField(default=0.0, verbose_name='Liquidated (PhP)', help_text='Must be the same as the amount released if unliquidated.')
	date_released = models.DateField()

	class Meta:
		verbose_name = 'Voucher'
		verbose_name_plural = 'Vouchers'

	def released_to(self):
		if self.allocation:
			return '%s:%s' % (self.allocation.grant.grant_type(), self.allocation.name)
		elif self.grant:
			return self.grant.grant_type()
		else:
			return self.description

	def disparity(self):
		return self.amount_released - self.amount_liquidated

	def clean(self):
		if not (self.description.strip() > 0 or self.allocation or self.grant):
			raise ValidationError('Description must be provided if allocation or grant is not indicated')
		if self.amount_liquidated > self.amount_released:
			raise ValidationError('Amount liquidated must be less than or equal to the amount released.')

	def __unicode__(self):
		return self.released_to()

#################################################################

class Scholarship(Grant):
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
		(PROPOSAL, 'Proposal Stage'),
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

	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})
	degree_program = models.ForeignKey(Degree_Program)
	adviser = models.ForeignKey(Person, related_name='adviser', null=True, blank=True)
	scholarship_status = models.CharField(max_length=5, choices=SCHOLARSHIP_STATUS_CHOICES, default=REG_ONGOING)
	high_degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, default=BS, verbose_name='Highest degree')
	high_degree_univ = models.ForeignKey(University, related_name='high_degree_univ', verbose_name="Highest degree's University")
	thesis_topic = models.CharField(max_length=350, blank=True)
	thesis_title = models.CharField(max_length=350, blank=True)
	thesis_status = models.CharField(max_length=5, choices=THESIS_STATUS_CHOICES, default=PROPOSAL)
	ce_schedule = models.DateField(null=True, blank=True, verbose_name='Candidacy Exam schedule')
	entry_grad_program = models.DateField(verbose_name='Entry to graduate program')
	end_grad_program = models.DateField(verbose_name='Date of graduation')
	lateral = models.BooleanField(default=False)
	cleared = models.BooleanField(default=False)

	def where(self):
		return self.degree_program.department.__unicode__()
	where.short_description = 'Department / University'

	def clean(self):
		if self.adviser == self.recipient:
			raise ValidationError('Adviser and scholar fields can not be the same.')
		if self.start_date == self.entry_grad_program and self.lateral:
			raise ValidationError('Entry to graduate and scholarship program can not be the same if lateral.')
		if self.start_date != self.entry_grad_program and not self.lateral:
			raise ValidationError('Entry to graduate and scholarship program must be the same if not lateral.')

	def grant_type(self):
		return 'ERDT Scholarship (%s Local)' % self.degree_program.degree

	def __unicode__(self):
		return self.degree_program.__unicode__()

class ERDT_Scholarship_Special(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

class Sandwich_Program(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

	class Meta:
		verbose_name = 'Sandwich Program'
		verbose_name_plural = 'Sandwich Programs'

	def grant_type(self):
		return 'Sandwich Program'

	def __unicode__(self):
		return self.description

class Postdoctoral_Fellowship(Grant):
	pass

class FRGT(Grant):
	pass

class FRDG(Grant):
	pass

class Visiting_Professor_Grant(Grant):
	distinguished = models.BooleanField(default=False)
	home_univerisy = models.CharField(max_length=150)
	host_university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})
	host_professor = models.ForeignKey(Person, related_name='host_professor')

#############################################################################################

class Equipment(Grant_Allocation_Release):
	# CONSUMABLE, EQUIPMENT, SERVICE, OTHER = 'CONSUMABLE', 'EQUIPMENT', 'SERVICE', 'OTHER'
	# ITEMTYPE_CHOICES = (
	# 	(CONSUMABLE, 'Consumable'),
	# 	(EQUIPMENT, 'Equipment'),
	# 	(SERVICE, 'Service'),
	# 	(OTHER, 'Other'),
	# )

	# item_type = models.CharField(max_length=50, choices=ITEMTYPE_CHOICES, default=OTHER, verbose_name='Item type')
	# quantity = models.FloatField(default=1.0, null=True, blank=True)
	location = models.CharField(max_length=150, blank=True)
	property_no =  models.CharField(max_length=50, blank=True, help_text='If funded by multiple grants, use the same property no for the same item.')
	status = models.CharField(max_length=150, blank=True)
	accountable = models.ForeignKey(Person, related_name='accountable')

	def __unicode__(self):
		return self.description

	def clean(self):
		# if not self.accountable:
		# 	raise ValidationError('Equipment item must have an assigned accountable person.')

		if self.accountable and self.accountable.profile_set.filter(role=Profile.ADVISER).count() == 0:
			raise ValidationError('Accountable person must have a Faculty Adviser profile.')

	class Meta:
		verbose_name = 'Equipment'
		verbose_name_plural = 'Equipments'

	
class Research_Dissemination(Grant_Allocation_Release):
	paper_title = models.CharField(max_length=250)
	conference_name = models.CharField(max_length=250)
	conference_loc = models.CharField(max_length=250)
	conference_date = models.DateField()

	class Meta:
		verbose_name = 'Research Dissemination'
		verbose_name_plural = 'Research Disseminations'

	def __unicode__(self):
		return '%s: %s' % (self.recipient, self.paper_title)