from django.db import models
from profiling.models import *
from django.utils.html import format_html, mark_safe
from datetime import datetime

class Report(models.Model):
	SUMMARY, FUND_RELEASES = 'SUMMARY', 'FUND_RELEASES'
	ALL_REPORT_CHOICES = (
		(SUMMARY, 'Summary'),
		(FUND_RELEASES, 'Fund Releases'),
	)

	name = models.CharField(max_length=250, unique=True, verbose_name='Report name')
	description = models.CharField(max_length=250, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	report_type = models.CharField(max_length=50, choices=ALL_REPORT_CHOICES, verbose_name='Report type')
	start_date = models.DateField(verbose_name='Start of period', help_text='Format: YYYY-MM-DD')
	end_date = models.DateField(verbose_name='End of period', help_text='Format: YYYY-MM-DD')
	active_only = models.BooleanField(default=True)

	class Meta:
		abstract=True

class Individual_Report(Report):
	person = models.ForeignKey(Person)

	class Meta:
		verbose_name = 'Individual Report'
		verbose_name_plural = 'Individual Reports'

	def create_report(self):
		out = u'<br/><br/><h3>%s</h3><p>Report type: %s<br/>Generated on: %s</p>' % (self.person.__unicode__(), 
			self.get_report_type_display(), datetime.today().ctime())
		try:
			my_grants = Grant.objects.filter(awardee_id=self.person.id)

			_inner_table =  ''

			for g in my_grants:
				grant_name = g.__unicode__()
				contract_period = '%s<br/>%s' % (g.start_date.strftime('%Y %b-%d'),g.end_date.strftime('%Y %b-%d'))
				summary = g.allocation_summary()
				_inner_table += '<tr><td><b>%s</b></td><td class="numeric">%s</td></tr><tr><td colspan="2">%s</td></tr>' % (grant_name, contract_period, summary)

			if my_grants.exists():
				out += '<h4>Grants Awarded</h4>'
				out += '<table class="sub-table">%s</table>' % _inner_table

			my_releases = Grant_Allocation_Release.objects.filter(payee_id=self.person.id)

			_inner_table = '<tr><td><b>Date Released</b></td><td><b>Particular</b></td><td><b>Released</b></td><td><b>Expenditure</b></td><td><b>Unexpended</b></td></tr>'

			for f in my_releases:
				date_released = f.date_released.strftime('%Y %b-%d')
				released = '%.2f' % f.amount_released
				expenditure = '%.2f' % f.amount_liquidated
				unexpended = '%.2f' % f.amount_unexpended()
				_inner_table += '<tr><td>%s</td><td>%s</td><td class="numeric">%s</td><td class="numeric">%s</td><td class="numeric">%s</td></tr>' % (date_released, f.particular(), released, expenditure, unexpended)

			if my_releases.exists():
				out += '<h4>Fund Releases</h4>'
				out += '<table class="sub-table table-bordered">%s</table>' % _inner_table

			out = format_html(mark_safe(out))
		except Exception as e:
			print 'Error at Individual_Report'
		return out

	def report_link(self):
		if self.id:
			url = '/create_individual_report_pdf/%d' % self.id
			return format_html(u'<a href="{}">%s</a>' % 'Report link', url)

	def __unicode__(self):
		return self.name

class Grant_Report(Report):
	grant = models.ForeignKey(Grant)

	def create_report(self):
		return ''

	def __unicode__(self):
		return self.name

class University_Report(Report):
	university = models.ForeignKey(University, limit_choices_to={'is_consortium':True})

	class Meta:
		verbose_name = 'University Report'
		verbose_name_plural = 'University Reports'

	def create_report(self):
		out = u'<h1>%s</h1> <br/> Created at %s. <br/><br/> <h2>Report</h2><br/>' % (self.university.__unicode__(), 
			self.created_at)
		out = format_html(mark_safe(out))
		return out

	def report_link(self):
		if self.id:
			url = '/create_university_report_pdf/%d' % self.id
			return format_html(u'<a href="{}">%s</a>' % 'Report link', url)

	def __unicode__(self):
		return self.name

class Consolidated_Report(Report):
	pass

	def create_report(self):
		return ''

	def __unicode__(self):
		return self.name
