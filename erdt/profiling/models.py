from django.db import models
from django.db.models import Q, F, Sum, SET_NULL, PROTECT
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from polymorphic import PolymorphicModel
from datetime import datetime, date
from smart_selects.db_fields import ChainedForeignKey as GF
from django.utils.html import format_html, mark_safe
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

	erdt_id = models.CharField(max_length=100, editable=False, unique=True, verbose_name='ERDT ID')
	user = models.ForeignKey(
		User, verbose_name='User account', null=True, blank=True, unique=True, on_delete=SET_NULL)
	photo = models.ImageField(upload_to='img', null=True, blank=True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	birthdate = models.DateField(help_text='Format: YYYY-MM-DD')
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)
	civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, default=SINGLE)
	address = models.CharField(max_length=250, verbose_name='Permanent address')
	address2 = models.CharField(max_length=250, verbose_name='Current address')
	email_address = models.EmailField(blank=True)
	landline_number = models.CharField(max_length=100, blank=True)
	mobile_number = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ('last_name', 'first_name', 'middle_name', 'erdt_id')

	def age(self):
		today = date.today()
		return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

	def name(self):
		return '%s, %s %s' % (self.last_name, self.first_name, self.middle_name)

	def my_link(self):
		if self.id:
			url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
			return format_html(u'<a href="{}">%s</a>' % self.__unicode__(), url)
		return self.__unicode__()

	def clean(self):
		if self.landline_number.strip() == '' and self.mobile_number.strip() == '' and self.email_address.strip() == '':
			raise ValidationError('Provide at least one contact number or an email address.')

	def save(self, *args, **kwargs):
		if not self.id:
			super(Person, self).save(*args, **kwargs)

		if self.id and (not self.erdt_id):
			today = date.today()
			self.erdt_id = '%.2d-%d%.4d' % ((today.year + 1) % 1000, today.weekday()+1, self.id % 1000)
		super(Person, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s, %s %s (%s)' % (self.last_name, self.first_name, self.middle_name, self.erdt_id)

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

	def clean_fields(self, exclude=None):
		if self.is_consortium and (not self.member_since):
			raise ValidationError('Specify membership date.')
		super(University, self).clean_fields(exclude)

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
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True}, on_delete=PROTECT)

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
	department = models.ForeignKey(Department, on_delete=PROTECT)

	class Meta:
		verbose_name = 'Degree Program'
		verbose_name_plural = 'Degree Programs'
		ordering = ('department', 'degree', 'program', )

	def __unicode__(self):
		return '%s %s, %s' % (self.degree, self.program, self.department.university.short_name)

class Subject(models.Model):
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True}, on_delete=PROTECT)
	title = models.CharField(max_length=100, verbose_name='Course title')
	code = models.CharField(max_length=20, blank=True, verbose_name='Course code')
	description = models.CharField(max_length=250, blank=True)
	units = models.FloatField(default=3.0)

	class Meta:
		ordering = ('title', 'university')

	def __unicode__(self):
		if self.code:
			return '(%s) %s: %s' % (self.code, self.title, self.university.short_name)	
		return '%s: %s' % (self.title, self.university.short_name)

	def clean(self):
		if not self.university.is_consortium:
			raise ValidationError('University must be an ERDT consortium member to add subjects.')

class Enrolled_Subject(models.Model):
	subject = models.ForeignKey(Subject, on_delete=PROTECT)
	scholar = models.ForeignKey(Person, on_delete=PROTECT)
	year_taken = models.DateField(help_text='Format: YYYY-MM-DD')
	eq_grade = models.FloatField(default=0.0, verbose_name='Grade')

	class Meta:
		verbose_name = 'Enrolled Subject'
		verbose_name_plural = 'Enrolled Subjects'
		ordering = ('year_taken', 'subject',)

	def __unicode__(self):
		return '%s: %s' % (self.scholar.__unicode__(), self.subject.__unicode__())

class Profile(models.Model):
	STUDENT, ADVISER, UNIV_ADMIN, CENTRAL_OFFICE, DOST, VISITING = 'STU', 'ADV', 'ADMIN', 'CENT', 'DOST', 'VISIT'
	ALL_ROLE_CHOICES = (
		(STUDENT, 'Student'),
		(ADVISER, 'Faculty'),
		(VISITING, 'Visiting Professor'),
		(UNIV_ADMIN, 'Consortium Administrator'),
		(CENTRAL_OFFICE, 'ERDT Central Office'),
		(DOST, 'DOST Office'),
	)
	ADMIN_ROLE_CHOICES = (
		(STUDENT, 'Student'),
		(ADVISER, 'Faculty'),
		(UNIV_ADMIN, 'Consortium Administrator'),
	)

	role = models.CharField(max_length=5, choices=ALL_ROLE_CHOICES, default=STUDENT)
	person = models.ForeignKey(Person)
	university = models.ForeignKey(
		University, limit_choices_to={'is_consortium':True}, 
		help_text='Leave blank for DOST or ERDT Central Office role.', null=True, blank=True)
	active = models.BooleanField(default=False)

	class Meta:
		unique_together = ('role', 'person',)
		ordering = ('person', 'role', 'university')

	def __unicode__(self):
		if self.university:
			return '%s as %s %s' % (self.person.name(), self.university.short_name, self.get_role_display())
		else:
			return '%s as %s' % (self.person.name(), self.get_role_display())

	def clean_fields(self, exclude=None):
		super(Profile, self).clean_fields(exclude)
		if self.role in (self.STUDENT, self.ADVISER, self.UNIV_ADMIN, self.VISITING):
			if self.university == None:
				raise ValidationError('Specify university of affiliation.')

	def save(self, *args, **kwargs):
		if self.role in (self.DOST, self.CENTRAL_OFFICE):
			self.university = None
		super(Profile, self).save(*args, **kwargs)

class Grant(PolymorphicModel):
	awardee = models.ForeignKey(Person, related_name='grants')
	description = models.CharField(max_length=250, blank=True)
	start_date = models.DateField(verbose_name='Start of contract', help_text='Format: YYYY-MM-DD')
	end_date = models.DateField(verbose_name='End of contract', help_text='Format: YYYY-MM-DD')
	record_manager = models.ForeignKey(University, limit_choices_to={'is_consortium':True}, null=True, blank=True, related_name='grants_managed', on_delete=SET_NULL)

	class Meta:
		verbose_name = 'Grant'
		verbose_name_plural = 'Grants'
		ordering = ('awardee', '-end_date')

	def grant_type(self):
		"""Returns the type of grant. Overridden by children."""
		return 'Grant'

	def awardee_link(self):
		return self.awardee.my_link()
	awardee_link.short_description = 'Awardee'

	def grant_link(self):
		label = self.grant_type()
		try:
			url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
			return format_html(u'<a href="{}">%s</a>' % label, url)
		except:
			pass
		return label
		
	grant_link.short_description = 'Grant type'

	def is_active(self):
		if not self.start_date:
			return -1
		today = date.today()
		return 1 if self.start_date <= today <= self.end_date else 0

	def total_budget(self):
		total_amount = self.grant_allocation_set.aggregate(Sum('amount')).values()[0]
		return total_amount if total_amount else 0.0
	total_budget.short_description = 'Budget'

	def total_released(self):
		total_amount = self.grant_allocation_release_set.aggregate(Sum('amount_released')).values()[0]
		return total_amount if total_amount else 0.0
	total_released.short_description = 'Released'

	def total_expenditure(self):
		total_amount = self.grant_allocation_release_set.aggregate(Sum('amount_liquidated')).values()[0]
		return total_amount if total_amount else 0.0
	total_expenditure.short_description = 'Expenditure'

	def total_unexpended(self):
		total_amount = 0.0
		for fund_release in self.grant_allocation_release_set.all():
			total_amount += fund_release.amount_unexpended()
		return total_amount
	total_unexpended.short_description = 'Unexpended'

	def total_unreleased(self):
		return self.total_budget() - self.total_released() + self.total_unexpended()
	total_unreleased.short_description = 'Unreleased'

	def allocation_summary(self):
		out = u'<tr> <td><b>Line Item</b></td> <td><b>App. Budget</b></td>  \
			<td><b>Released</b></td> <td><b>Unexpended</b></td> <td><b>Unreleased</b></td> </tr>'

		_temp =  '<td> %s </td>' + ('<td class="numeric"> %s </td> ' * 4)

		t_allotment, t_released, t_unexpended, t_unreleased = (0.0, 0.0, 0.0, 0.0)

		for allocation in self.grant_allocation_set.all():
			alloc_comps = allocation.get_computations().split()

			f_released = float(alloc_comps[0])
			f_unxpended = float(alloc_comps[2])
			f_unreleased = float(alloc_comps[3])
 			out = out + '<tr> %s </tr>' % (_temp % (allocation.get_name_display(), '%.2f' % allocation.amount, 
				'%.2f' % f_released, '%.2f' % f_unxpended, '%.2f' % f_unreleased))

			t_allotment += allocation.amount
			t_released += float(alloc_comps[0])
			t_unexpended += float(alloc_comps[2])
			t_unreleased += float(alloc_comps[3])

		totals = ('<tr> %s </tr>' % _temp) % ('<b>Total</b>', '<b>%.2f</b>' % t_allotment, 
			'<b>%.2f</b>' % t_released, '<b>%.2f</b>' % t_unexpended, '<b>%.2f</b>' % t_unreleased)

		out = u'<table class="table table-bordered table-condensed table-striped"><thread> %s %s \
			</thread></table>' % (out, totals)

		return format_html(mark_safe(out))
	allocation_summary.short_description = 'Budget summary'

	def __unicode__(self):
		return self.grant_type()

	def clean(self):
		if self.start_date > self.end_date:
			raise ValidationError('Start of contract date must precede or the same as the end of contract date.')

class Grant_Allocation(models.Model):
	TUITION_FEE, STIPEND, BOOK_ALLOWANCE, TRANSPORTATION_ALLOWANCE = 'TUITION', 'STIPEND', 'BOOK_ALW', 'TRANSP_ALW'
	THESIS_ALLOWANCE, RESEARCH_GRANT, RESEARCH_DISSEMINATION_ALLOWNACE = 'THESIS_ALW', 'RESEARCH_GNT', 'DISSEMINATION_ALLW'
	MENTORS_FEE, AIRFARE, RESEARCH_EXPENSES, PRETRAVEL_EXPENSES = 'MENTORS_FEE', 'AIRFARE', 'RESEARCH_EXP', 'PRETRAVEL_EXP'
	LIVING_EXPENSES, RELOCATE_ALLOWANCE = 'LIVING_EXP', 'RELOCATE_ALW'
	MEDICAL_INSURANCE, TRAVEL_INSURANCE, MEDICAL_TRAVEL_INSURANCE = 'MEDICAL_INS', 'TRAVEL_INS', 'MED_TRAV_INS'
	CONFERENCE_REG, DSA, PROFESSIONAL_FEE = 'CONFE_REG', 'DSA', 'PROF_FEE'

	GRANT_ALLOC_CHOICES = (
		(TUITION_FEE, 'Tuition Fees'),
		(STIPEND, 'Stipend'),
		(BOOK_ALLOWANCE, 'Book Allowance'),
		(TRANSPORTATION_ALLOWANCE, 'Transportation Allow.'),
		(THESIS_ALLOWANCE, 'Thesis/Dissert. Allow.'),
		(RESEARCH_GRANT, 'Research Grant'),
		(RESEARCH_DISSEMINATION_ALLOWNACE, 'Research Diss. Allow.'),
		(MENTORS_FEE, 'Mentor\'s Fee'),
		(AIRFARE, 'Airfare'),
		(RESEARCH_EXPENSES, 'Research Expenses'),
		(PRETRAVEL_EXPENSES, 'Pre-travel Expenses'),
		(LIVING_EXPENSES, 'Living Expenses'),
		(RELOCATE_ALLOWANCE, 'Relocation Allowance'),
		(MEDICAL_INSURANCE, 'Medical Insurance'),
		(TRAVEL_INSURANCE, 'Travel Insurance'),
		(MEDICAL_TRAVEL_INSURANCE, 'Medical/Travel Insur.'),
		(CONFERENCE_REG, 'Conference Reg.'),
		(DSA, 'DSA'),
		(PROFESSIONAL_FEE, 'Professional Fee')
	)
	SCHOLARSHIP_ALLOC_CHOICES = (
		(TUITION_FEE, 'Tuition Fees'),
		(STIPEND, 'Stipend'),
		(BOOK_ALLOWANCE, 'Book Allowance'),
		(TRANSPORTATION_ALLOWANCE, 'Transportation Allow.'),
		(THESIS_ALLOWANCE, 'Thesis/Dissert. Allow.'),
		(RESEARCH_GRANT, 'Research Grant'),
		(RESEARCH_DISSEMINATION_ALLOWNACE, 'Research Diss. Allow.'),
		(MENTORS_FEE, 'Mentor\'s Fee'),
	)
	SANDWICH_ALLOC_CHOICES = (
		(AIRFARE, 'Airfare'),
		(MEDICAL_INSURANCE, 'Health Insurance'),
		(RESEARCH_EXPENSES, 'Research Expenses'),
		(PRETRAVEL_EXPENSES, 'Pre-travel Expenses'),
		(LIVING_EXPENSES, 'Living Expenses'),
		(RELOCATE_ALLOWANCE, 'Relocation Allowance'),
	)
	SCHOLARSHIP2_ALLOC_CHOICES = (
		(TUITION_FEE, 'Tuition Fees'),
		(PRETRAVEL_EXPENSES, 'Pre-travel Expenses'),
		(AIRFARE, 'Airfare'),
		(RELOCATE_ALLOWANCE, 'Relocation Allowance'),
		(BOOK_ALLOWANCE, 'Book Allowance'),
		(STIPEND, 'Stipend'),
		(MEDICAL_TRAVEL_INSURANCE, 'Medical/Travel Insur.'),
		(THESIS_ALLOWANCE, 'Dissertation Allowance'),
		(RESEARCH_DISSEMINATION_ALLOWNACE, 'Research Diss. Allow.'),
	)
	POSTDOCTORAL_ALLOC_CHOICES = (
		(AIRFARE, 'Airfare'),
		(RESEARCH_EXPENSES, 'Research Expenses'),
		(PRETRAVEL_EXPENSES, 'Pre-travel Expenses'),
		(LIVING_EXPENSES, 'Living Expenses'),
	)
	FRGT_ALLOC_CHOICES = (
		(RESEARCH_GRANT, 'Research Grant'),
	)
	FRDG_ALLOC_CHOICES = (
		(CONFERENCE_REG, 'Conference Registration'),
		(DSA, 'DSA'),
		(AIRFARE, 'Airfare'),
		(TRAVEL_INSURANCE, 'Travel Insurance'),
	)
	VP_ALLOC_CHOICES = (
		(AIRFARE, 'Airfare'),
		(TRAVEL_INSURANCE, 'Travel Insurance'),
		(PROFESSIONAL_FEE, 'Professional Fee'),
		(TRANSPORTATION_ALLOWANCE, 'Transportation Allow.'),
		(DSA, 'DSA'),
	)

	grant = models.ForeignKey(Grant)
	name = models.CharField(max_length=150, choices=GRANT_ALLOC_CHOICES,verbose_name="Line item")
	description = models.CharField(max_length=350, blank=True)
	amount = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Line Item'
		verbose_name_plural = 'Line Items'
		unique_together = ('grant', 'name',)

	def get_computations(self):
		total_released, total_expenditure, total_unexpended, total_unreleased = 0.0, 0.0, 0.0, 0.0

		for fund_release in self.grant_allocation_release_set.all():
			total_released += fund_release.amount_released
			total_expenditure += fund_release.amount_liquidated
			total_unexpended +=  fund_release.amount_unexpended()

		total_unreleased = self.amount - total_released + total_unexpended

		return ' '.join((str(total_released), str(total_expenditure), str(total_unexpended), str(total_unreleased)))

	def total_released(self):
		return self.get_computations().split()[0]
	total_released.short_description = 'Released'
	def total_expenditure(self):
		return self.get_computations().split()[1]
	total_expenditure.short_description = 'Expenditure'
	def total_unexpended(self):
		return self.get_computations().split()[2]
	total_unexpended.short_description = 'Unexpended'
	def total_unreleased(self):
		return self.get_computations().split()[3]
	total_unreleased.short_description = 'Unreleased'

	def __unicode__(self):
		return '%s: %s' % (self.grant.grant_type(), self.get_name_display())

class Grant_Allocation_Release(PolymorphicModel):
	CONSUMABLE, EQUIPMENT, SERVICE, OTHER, RS = 'CONSUMABLE', 'EQUIPMENT', 'SERVICE', 'OTHER', 'DISSEMINATION'
	ITEMTYPE_CHOICES = (
		(CONSUMABLE, 'Consumable'),
		(SERVICE, 'Service'),
		(OTHER, 'Other'),
	)

	ITEMTYPE_CHOICES_ALL = ITEMTYPE_CHOICES + ((RS, 'Reasearch Dissemination'), (EQUIPMENT, 'Equipment'),)

	item_type = models.CharField(max_length=50, choices=ITEMTYPE_CHOICES_ALL, blank=True, verbose_name='Type', help_text='For research grant fund releases only. Leave blank otherwise.')
	payee = models.ForeignKey(Person, related_name='fund_releases', on_delete=PROTECT)
	grant = GF(Grant, chained_field='payee', chained_model_field='awardee', show_all=False, auto_choose=True, verbose_name='Funding grant', on_delete=PROTECT)
	allocation = GF(Grant_Allocation, chained_field='grant', chained_model_field='grant', auto_choose=True, verbose_name='Funding line item', on_delete=PROTECT)
	description = models.CharField(max_length=350, blank=True)
	amount_released = models.FloatField(default=0.0, verbose_name='Released')
	amount_liquidated = models.FloatField(default=0.0, verbose_name='Liquidated', help_text='0.0 means unliquidated.')
	date_released = models.DateField(help_text='Format: YYYY-MM-DD', verbose_name='Date Released')

	class Meta:
		verbose_name = 'Fund Release'
		verbose_name_plural = 'Fund Releases'
		ordering = ('-date_released', 'payee',)

	def payee_sub(self):
		""" Polymorphic model could not call overridden method if queried with payee. 
			Use this medthod to display payee's name """
		return self.payee.name()
		#return '%s, %s %s' % (self.payee.last_name, self.payee.first_name, self.payee.middle_name)
	payee_sub.short_description = 'Payee'
	payee_sub.admin_order_field = 'payee'

	def particular(self):
		if self.description.strip() != '':
			return '%s (%s)' % (self.allocation.__unicode__(), self.description)
		else:
			return self.allocation.__unicode__()
	particular.admin_order_field = 'date_released'

	def payee_link(self):
		return self.payee.my_link()
	payee_link.short_description = 'Payee'
	payee_link.admin_order_field = 'payee'

	def release_link(self):
		url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
		return format_html(u'<a href="{}">%s</a>' % self.particular(), url)
	release_link.short_description = 'Particular'	

	def amount_unexpended(self):
		if self.amount_liquidated > 0.0 :
			return self.amount_released - self.amount_liquidated 
		else:
			return 0.0
	amount_unexpended.short_description = 'Unexpended'

	def clean_fields(self, exclude=None):
		if self.amount_liquidated > self.amount_released:
			raise ValidationError('Expenditure must be less than or equal to the amount released.')
		super(Grant_Allocation_Release, self).clean_fields(exclude)

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

	university = models.ForeignKey(
		University, limit_choices_to={'is_consortium':True}, on_delete=PROTECT)
	degree_program = GF(
		Degree_Program, chained_field='university', chained_model_field='department__university', 
		on_delete=PROTECT)
	adviser = models.ForeignKey(
		Person, related_name='advisees', null=True, blank=True, on_delete=PROTECT)
	scholarship_status = models.CharField(
		max_length=5, choices=SCHOLARSHIP_STATUS_CHOICES, default=REG_ONGOING)
	high_degree = models.CharField(
		max_length=5, choices=DEGREE_CHOICES, default=BS, verbose_name='Highest degree')
	high_degree_univ = models.ForeignKey(
		University, related_name='high_degree_univ', verbose_name="Highest degree's University", 
		on_delete=PROTECT)
	thesis_topic = models.CharField(max_length=350, blank=True)
	thesis_title = models.CharField(max_length=350, blank=True)
	thesis_status = models.CharField(max_length=5, choices=THESIS_STATUS_CHOICES, default=PROPOSAL)
	ce_schedule = models.DateField(null=True, blank=True, verbose_name='Candidacy Exam schedule', 
		help_text='Format: YYYY-MM-DD')
	entry_grad_program = models.DateField(verbose_name='Entry to graduate program', 
		help_text='Format: YYYY-MM-DD')
	end_grad_program = models.DateField(verbose_name='Date of graduation', 
		help_text='Format: YYYY-MM-DD')
	lateral = models.BooleanField(default=False)
	cleared = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Scholarship (Local)'
		verbose_name_plural = 'Scholarships (Local)'

	def clean(self):
		super(Scholarship, self).clean()

		if self.adviser == self.awardee:
			raise ValidationError('Scholarship grant awardee and adviser fields can not be the same.')
		if self.start_date == self.entry_grad_program and self.lateral:
			raise ValidationError('Entry to graduate and scholarship program can not be the same if lateral.')
		if self.start_date != self.entry_grad_program and not self.lateral:
			raise ValidationError('Entry to graduate and scholarship program must be the same if not lateral.')

	def grant_type(self):
		return 'Scholarship (%s, %s)' % (self.degree_program.degree, self.degree_program.department.university.short_name)

	def is_active(self):
		if self.scholarship_status == Scholarship.ON_EXT:
			return 2
		return super(Scholarship, self).is_active()

class ERDT_Scholarship_Special(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

	class Meta:
		verbose_name = 'Scholarship (PhD Abroad)'
		verbose_name_plural = 'Scholarships (PhD Abroad)'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'Scholarship (Abroad PhD)'

class Sandwich_Program(Grant):
	host_university = models.CharField(max_length=150)
	host_professor = models.CharField(max_length=150)

	class Meta:
		verbose_name = 'Sandwich Program'
		verbose_name_plural = 'Sandwich Programs'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'Sandwich %s' % str(self.start_date.year)

class Postdoctoral_Fellowship(Grant):
	class Meta:
		verbose_name = 'Postdoctoral Fellowship'
		verbose_name_plural = 'Postdoctoral Fellowships'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'Postdoctoral %s' % str(self.start_date.year)

class FRGT(Grant):
	class Meta:
		verbose_name = 'Faculty Research Grant'
		verbose_name_plural = 'Faculty Research Grants'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'FRG %s' % str(self.start_date.year)

class FRDG(Grant):
	class Meta:
		verbose_name = 'Faculty Research Diss Grant'
		verbose_name_plural = 'Faculty Research Diss Grants'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'FRDG %s' % str(self.start_date.year)

class Visiting_Professor_Grant(Grant):
	distinguished = models.BooleanField(default=False)
	home_university = models.CharField(max_length=150)
	host_university = models.ForeignKey(University, limit_choices_to={'is_consortium':True}, on_delete=PROTECT)
	host_professor = models.ForeignKey(Person, related_name='visiting_professor_guests', on_delete=PROTECT)

	class Meta:
		verbose_name = 'Visiting Professor Grant'
		verbose_name_plural = 'Visiting Professor Grants'
		ordering = ('-start_date', 'awardee',)

	def grant_type(self):
		return 'Visiting %s' % str(self.start_date.year)


#############################################################################################

class Equipment(Grant_Allocation_Release):
	CONDEMNED, WORKING, FOR_REPAIR = 'CONDEMNED', 'WORKING', 'FOR_REPAIR'
	STATUS_CHOICES = (
		(WORKING, 'Working'),
		(FOR_REPAIR, 'For Repair'),
		(CONDEMNED,' Condemned'),
	)

	location = models.CharField(max_length=150)
	property_no =  models.CharField(max_length=50, help_text='If funded by multiple grants, use the same property no for the same item.')
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=WORKING)
	accountable = models.ForeignKey(Person, related_name='equipments', on_delete=PROTECT)
	surrendered = models.BooleanField(default=False, verbose_name='Donated')

	def accountable_link(self):
		return self.accountable.my_link()
	accountable_link.short_description = 'Accountable'
	accountable_link.admin_order_field = 'accountable'

	def accountable_sub(self):
		""" Polymorphic model could not call overridden method if queried with accountable. 
			Use this medthod to display accountable's name """
		return self.accountable.name()
		#return '%s, %s %s' % (self.accountable.last_name, self.accountable.first_name, self.accountable.middle_name)
	accountable_sub.short_description = 'Accountable'
	accountable_sub.admin_order_field = 'accountable'

	def description_link(self):
		url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
		return format_html(u'<a href="{}">%s</a>' % self.description, url)
	description_link.short_description = 'Description'

	class Meta:
		verbose_name = 'Equipment'
		verbose_name_plural = 'Equipments'

	def clean_fields(self, exclude=None):
		super(Equipment, self).clean_fields(exclude)
		if self.description.strip() == '':
			raise ValidationError('Description cannot be blank for equipment.')

	def save(self, *args, **kwargs):
		self.item_type = Grant_Allocation_Release.EQUIPMENT
		super(Equipment, self).save(*args, **kwargs)
	
class Research_Dissemination(Grant_Allocation_Release):
	paper_title = models.CharField(max_length=250)
	conference_name = models.CharField(max_length=250)
	conference_loc = models.CharField(max_length=250, verbose_name='Conference location')
	conference_date = models.DateField(help_text='Format: YYYY-MM-DD')

	class Meta:
		verbose_name = 'Research Dissemination'
		verbose_name_plural = 'Research Disseminations'

	def save(self, *args, **kwargs):
		self.item_type = Grant_Allocation_Release.RS
		super(Research_Dissemination, self).save(*args, **kwargs)

###
