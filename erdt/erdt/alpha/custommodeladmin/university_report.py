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

class UniversityReportAdmin(ERDTModelAdmin):
    readonly_fields = ('active_only', 'create_report')
    #change_form_template = 'admin/reporting/change_form_pdf.html'

