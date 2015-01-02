from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from polymorphic import PolymorphicModel
from datetime import date
from smart_selects.db_fields import ChainedForeignKey as GF
from django.utils.html import format_html
from django.core.urlresolvers import reverse

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

	user = models.ForeignKey(User, verbose_name='User account', null=True, blank=True, unique=True) 
	photo = models.ImageField(upload_to='img', null=True, blank=True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	birthdate = models.DateField(help_text='Format: YYYY-MM-DD')
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)
	civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, default=SINGLE)
	address = models.CharField(max_length=250)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=100, blank=True)
	mobile_number = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ('last_name', 'first_name', 'middle_name')

	def age(self):
		today = date.today()
		return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

	def clean(self):
		if self.landline_number.strip() == '' and self.mobile_number.strip() == '' and self.email_address.strip() == '':
			raise ValidationError('Provide at least one contact number or an email address.')

	def __unicode__(self):
		return '%s, %s %s' % (self.last_name, self.first_name, self.middle_name)

class University(models.Model):
	photo = models.ImageField(upload_to='univ_seal', null=True, blank=True)
	name = models.CharField(max_length=150)
	short_name = models.CharField(max_length=10, blank=True)
	is_consortium = models.BooleanField(default=False, verbose_name='ERDT Consortium')
	member_since = models.DateField(null=True, blank=True, help_text='Format: YYYY-MM-DD') 
	address = models.CharField(max_length=100, blank=True)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=100, blank=True)
	no_semester = models.IntegerField(default=2, null=True, blank=True, verbose_name='No of semester per SY')
	with_summer = models.BooleanField(default=False, verbose_name='With summer semester')

	def clean(self):
		if self.is_consortium and (not self.member_since):
			raise ValidationError('Specify membership date.')

	def save(self, *args, **kwargs):
		if not self.is_consortium:
			self.member_since = None
		super(University, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Universities'
		ordering = ('-is_consortium', 'name', )

	def __unicode__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=150)
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=50, blank=True)
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})

	class Meta:
		ordering = ('university', 'name')

	def __unicode__(self):
		return '%s, %s' % (self.name, self.university.short_name)

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
		ordering = ('department', 'degree', 'program', )

	def __unicode__(self):
		return '%s %s, %s' % (self.degree, self.program, self.department.university.short_name)

class Subject(models.Model):
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})
	title = models.CharField(max_length=100, verbose_name='Course title')
	code = models.CharField(max_length=20, blank=True, verbose_name='Course code')
	description = models.CharField(max_length=250, blank=True)
	units = models.FloatField(default=3.0)

	class Meta:
		ordering = ('title', 'university')

	def __unicode__(self):
		return '%s: %s' % (self.title, self.university.short_name)

	def clean(self):
		if not self.university.is_consortium:
			raise ValidationError('University must be an ERDT consortium member to add subjects.')

class Enrolled_Subject(models.Model):
	subject = models.ForeignKey(Subject)
	scholar = models.ForeignKey(Person)
	year_taken = models.DateField(help_text='Format: YYYY-MM-DD')
	sem_taken = models.IntegerField(default=1, verbose_name='Semester taken')
	eq_grade = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Enrolled Subject'
		verbose_name_plural = 'Enrolled Subjects'
		ordering = ('sem_taken', 'subject',)

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
		ordering = ('person', 'role', 'university')

	def __unicode__(self):
		if self.university:
			return '%s as %s %s' % (self.person, self.university.short_name, self.get_role_display())
		else:
			return '%s as %s' % (self.person, self.get_role_display())

	def clean(self):
		if self.role in (self.DOST, self.CENTRAL_OFFICE):
			self.university = None
		elif self.role in (self.STUDENT, self.ADVISER, self.UNIV_ADMIN):
			if self.university == None:
				raise ValidationError('Specify university of affiliation.')

class Grant(PolymorphicModel):
	awardee = models.ForeignKey(Person, related_name='awardee')
	description = models.CharField(max_length=250, blank=True)
	start_date = models.DateField(verbose_name='Start of contract', help_text='Format: YYYY-MM-DD')
	end_date = models.DateField(verbose_name='End of contract', help_text='Format: YYYY-MM-DD')
	allotment = models.FloatField(default=0.0, verbose_name='Allotment (PhP)')

	class Meta:
		verbose_name = 'Grant'
		verbose_name_plural = 'Grants'
		ordering = ('awardee', '-end_date')

	def grant_type(self):
		"""Returns the type of grant. Overridden by children."""

		return 'Grant'

	def awardee_link(self):
		url = reverse('admin:profiling_person_change', args=(self.awardee.id,))
		return format_html(u'<a href="{}" target=_blank>%s</a>' % self.awardee, url)
	awardee_link.short_description = 'Awardee'

	def grant_link(self):
		url = self.grant_type()

		if self.grant_type().startswith('Scholarship (Local'):
			url = reverse('admin:profiling_scholarship_change', args=(self.id,))
		elif self.grant_type().startswith('Sandwich'):
			url = reverse('admin:profiling_sandwich_program_change', args=(self.id,))
		else:
			return url
		return format_html(u'<a href="{}" target=_blank>%s</a>' % self.grant_type(), url)
	grant_link.short_description = 'Grant type'

	def is_active(self):
		return 1 if (self.start_date <= date.today() <= self.end_date) else 0

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

	def balance(self):
		return self.allotment - self.total_liquidated()
	balance.short_description = 'Balance (PhP)'

	def __unicode__(self):
		return '%s: %s' % (self.grant_type(), self.awardee.__unicode__())

	def clean(self):
		if self.start_date > self.end_date:
			raise ValidationError('Start of contract date must precede or the same as the end of contract date.')

class Grant_Allocation(models.Model):
	grant = models.ForeignKey(Grant)
	name = models.CharField(max_length=150, verbose_name="Line item")
	description = models.CharField(max_length=350, blank=True)
	amount = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Grant Allocation'
		verbose_name_plural = 'Grant Allocations'

	def __unicode__(self):
		return '%s: %s' % (self.grant.grant_type(), self.name)

class Grant_Allocation_Release(PolymorphicModel):
	payee = models.ForeignKey(Person, related_name='payee')
	grant = GF(Grant, chained_field='payee', chained_model_field='awardee', show_all=False, auto_choose=True) #models.ForeignKey(Grant)
	allocation = GF(Grant_Allocation, chained_field='grant', chained_model_field='grant', on_delete=models.CASCADE)
	description = models.CharField(max_length=350, blank=True)
	amount_released = models.FloatField(default=0.0, verbose_name='Released (PhP)')
	amount_liquidated = models.FloatField(default=0.0, verbose_name='Liquidated (PhP)', help_text='Must be the same as the amount released if unliquidated.')
	date_released = models.DateField(help_text='Format: YYYY-MM-DD')

	class Meta:
		verbose_name = 'Fund Release'
		verbose_name_plural = 'Fund Releases'
		ordering = ('-date_released', 'payee',)

	def particular(self):
		if self.description.strip() != '':
			return '%s (%s)' % (self.allocation.__unicode__(), self.description)
		else:
			return self.allocation.__unicode__()

	def payee_link(self):
		url = reverse('admin:profiling_person_change', args=(self.payee.id,))
		return format_html(u'<a href="{}">%s</a>' % self.payee.__unicode__(), url)
	payee_link.short_description = 'Payee'

	def release_link(self):
		url = reverse('admin:profiling_grant_allocation_release_change', args=(self.id,))
		return format_html(u'<a href="{} target=_blank">%s</a>' % self.particular(), url)
	release_link.short_description = 'Particular'

	def the_who(self):
		""" Polymorphic model could not call overridden method if queried with payee. 
			Use this medthod to display payee's name """
		return '%s, %s %s' % (self.payee.last_name, self.payee.first_name, self.payee.middle_name)
	the_who.short_description = 'Payee'
	the_who.admin_order_field = 'payee'

	def disparity(self):
		return self.amount_released - self.amount_liquidated
	disparity.short_description = 'Disparity (PhP)'

	def clean(self):
		if (self.payee != self.grant.awardee) or (self.grant != self.allocation.grant):
			raise ValidationError('Payee, grant awardee, and grant allocation must be consistent.')
		if self.amount_liquidated > self.amount_released:
			raise ValidationError('Amount liquidated must be less than or equal to the amount released.')
		if (self.amount_liquidated != self.amount_released) and (self.amount_liquidated == 0.0):
			raise ValidationError('Lidquidated amount cannot be zero.')

	def __unicode__(self):
		return self.particular()

#################################################################

class Scholarship(Grant):
	AB, MA, BS, MS, MD, PHD, MENGG, DENGG, =  'AB', 'MA', 'BS', 'MS', 'MD','PHD', 'MEngg', 'DEngg'
	DEGREE_CHOICES = (
		(BS, 'Bachelor of Science'),
		(MS, 'Master of Science'),
		(PHD, 'Doctor of Philosophy'),
		(MENGG, 'Master of Engineering'),
		(DENGG, 'Doctor of Engineering'),
		(MD, 'Doctor of Medicine'),
		(AB, 'Bachelor of Arts'),
		(MA, 'Master of Arts'),
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
	degree_program = GF(Degree_Program, chained_field='university', chained_model_field='department__university')
	adviser = models.ForeignKey(Person, related_name='adviser', null=True, blank=True)
	scholarship_status = models.CharField(max_length=5, choices=SCHOLARSHIP_STATUS_CHOICES, default=REG_ONGOING)
	high_degree = models.CharField(max_length=5, choices=DEGREE_CHOICES, default=BS, verbose_name='Highest degree')
	high_degree_univ = models.ForeignKey(University, related_name='high_degree_univ', verbose_name="Highest degree's University")
	thesis_topic = models.CharField(max_length=350, blank=True)
	thesis_title = models.CharField(max_length=350, blank=True)
	thesis_status = models.CharField(max_length=5, choices=THESIS_STATUS_CHOICES, default=PROPOSAL)
	ce_schedule = models.DateField(null=True, blank=True, verbose_name='Candidacy Exam schedule', help_text='Format: YYYY-MM-DD')
	entry_grad_program = models.DateField(verbose_name='Entry to graduate program', help_text='Format: YYYY-MM-DD')
	end_grad_program = models.DateField(verbose_name='Date of graduation', help_text='Format: YYYY-MM-DD')
	lateral = models.BooleanField(default=False)
	cleared = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Local Scholarship'
		verbose_name_plural = 'Local Scholarships'

	def clean(self):
		super(Scholarship, self).clean()

		if self.adviser == self.awardee:
			raise ValidationError('Scholarship grant awardee and adviser fields can not be the same.')
		if self.start_date == self.entry_grad_program and self.lateral:
			raise ValidationError('Entry to graduate and scholarship program can not be the same if lateral.')
		if self.start_date != self.entry_grad_program and not self.lateral:
			raise ValidationError('Entry to graduate and scholarship program must be the same if not lateral.')

	def grant_type(self):
		return 'Scholarship (Local %s)' % self.degree_program.degree

	def is_active(self):
		if self.scholarship_status == Scholarship.ON_EXT:
			return 2
		return super(Scholarship, self).is_active()

	def __unicode__(self):
		return self.grant_type()

class ERDT_Scholarship_Special(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

class Sandwich_Program(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

	class Meta:
		verbose_name = 'Sandwich Program'
		verbose_name_plural = 'Sandwich Programs'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'Sandwich %s' % str(self.start_date.year)

	def year(self):
		return self.start_date.year
	year.admin_order_field = '-start_date'

	def __unicode__(self):
		return self.grant_type()

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
	surrendered = models.BooleanField(default=False)

	def __unicode__(self):
		return self.particular()

	class Meta:
		verbose_name = 'Equipment'
		verbose_name_plural = 'Equipments'
	
class Research_Dissemination(Grant_Allocation_Release):
	paper_title = models.CharField(max_length=250)
	conference_name = models.CharField(max_length=250)
	conference_loc = models.CharField(max_length=250)
	conference_date = models.DateField(help_text='Format: YYYY-MM-DD')

	class Meta:
		verbose_name = 'Research Dissemination'
		verbose_name_plural = 'Research Disseminations'

	def __unicode__(self):
		return '%s: %s' % (self.payee, self.paper_title)

###