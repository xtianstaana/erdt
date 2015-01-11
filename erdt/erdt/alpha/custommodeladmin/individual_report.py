from erdt.alpha.custommodeladmin.globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions, HORIZONTAL, VERTICAL
from django.contrib.admin.options import InlineModelAdmin
from django import forms
from django.forms.widgets import *
from suit.widgets import *
from django.core.urlresolvers import resolve, reverse
from django_select2.widgets import *
from django.utils.translation import ugettext_lazy as _

class IndividualReportAdmin(ERDTModelAdmin):
    readonly_fields = ('create_report',)
    exclude = ('active_only', 'name', 'report_type', 'created_at', 'start_date', 'end_date', 'person')
    #change_form_template = 'admin/reporting/change_form_pdf.html'

    def get_change_form_template(self, request, obj=None):
    	if obj:
    		return 'admin/reporting/change_form_pdf.html'
		return super(IndividualReportAdmin, self).get_change_form_template(request, obj)
