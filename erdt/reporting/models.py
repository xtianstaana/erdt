from django.db import models
from profiling.models import *
from django.db.models import Q, F, Sum
from django.utils.html import format_html, mark_safe
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

# Create your models here.


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
		out = u'<h2>%s</h2><p>Report created at %s.</p><h3>Grants Awarded</h3>' % (self.person.__unicode__(), 
			self.created_at)
		try:
			my_grants = Grant.objects.filter(awardee_id=self.person.id)
			_inner_table =  ''
			for g in my_grants:
				_inner_table += '<tr><td><b>%s</b></td></tr><tr><td>%s</td></tr>' % (g.__unicode__(),g.allocation_summary())
			out += '<table>%s</table>' % _inner_table
			out = format_html(mark_safe(out))
		except Exception as e:
			print 'Error at Individual_Report'
		return out
	create_report.short_description = ''

class Grant_Report(Report):
	grant = models.ForeignKey(Grant)

	def create_report(self):
		return ''

class University_Report(Report):
	university = models.ForeignKey(University)

	class Meta:
		verbose_name = 'University Report'
		verbose_name_plural = 'University Reports'

	def create_report(self):
		out = u'<h1>%s</h1> <br/> Created at %s. <br/><br/> <h2>Report</h2><br/>' % (self.university.__unicode__(), 
			self.created_at)
		out = format_html(mark_safe(out))
		return out

class Consolidated_Report(Report):
	pass

	def create_report(self):
		return ''
