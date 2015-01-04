"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Grant Allocation Release
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django_select2.widgets import *


class MyGrantAllocationReleaseForm(forms.ModelForm):
    class Meta:
        model = Grant_Allocation_Release
        fields = '__all__'
        widgets = {
            'payee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class GrantAllocationReleaseAdmin(ERDTModelAdmin):
    form = MyGrantAllocationReleaseForm
    model = Grant_Allocation_Release
    list_display = ('date_released', 'particular', 'payee', )

    def get_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation', 'description', 'item_type', 'amount_released', 'amount_liquidated', 'date_released',)
        return ('payee', 'grant', 'allocation', 'description' ,'item_type', 'amount_released', 'amount_liquidated', 'date_released', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation')
        return super(GrantAllocationReleaseAdmin, self).get_readonly_fields(request, obj)