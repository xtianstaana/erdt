"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Scholarship
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


class AllocationInline(TabularInline):
    model = Grant_Allocation
    extra = 0
    suit_classes = 'suit-tab suit-tab-allocation'

class ScholarshipAdmin(ERDTModelAdmin):
    inlines = [AllocationInline]
    list_display = ('awardee', 'degree_program', 'where', 'scholarship_status')
    list_filter = ('degree_program__department__university__name', 'scholarship_status')
    readonly_fields = ('awardee',)

    formfield_overrides = {
       models.ForeignKey: {'widget': LinkedSelect},
    }

    fieldsets = [
        (None, {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('awardee', 'start_date', 'end_date', 'total_amount', 'description', 'scholarship_status', 'lateral', 'cleared'),
            }),
        ('Program Details', {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('university', 'degree_program', 'entry_grad_program' , 'end_grad_program', 'ce_schedule'),
            }),
        ('Educational Background', {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('high_degree_univ', 'high_degree',),
            }),
        (None, {
            'classes' : ('suit-tab', 'suit-tab-thesis'),
            'fields' : ('adviser', 'thesis_status', 'thesis_title', 'thesis_topic'),
            }),

    ]

    suit_form_tabs = (('general', 'General'), ('thesis', 'Thesis / Dissertation Information'), ('allocation', 'Scholarship Fund Allocations'))

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(ScholarshipAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return qs.filter(scholar__user = request.user.id)
            else:
                return qs
        except:
            return qs