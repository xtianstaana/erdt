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
from django_select2.widgets import *

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect

class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    fk = 'grant'
    extra = 0
    max_num = 0
    fields = ('release_link', 'date_released', 'amount_released', 'amount_liquidated', 'disparity')
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-releases'

class AllocationInline(TabularInline):
    model = Grant_Allocation
    extra = 0
    suit_classes = 'suit-tab suit-tab-allocation'

class MyScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = '__all__'
        widgets = {
            'awardee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'adviser' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class ScholarshipAdmin(ERDTModelAdmin):
    form = MyScholarshipForm
    inlines = [AllocationInline, ReleaseInline]
    list_display = ('degree_program', 'awardee_link', 'scholarship_status','cleared')
    list_filter = ('degree_program__department__university__name', 'scholarship_status')

    formfield_overrides = {
       models.ForeignKey: {'widget': LinkedSelect},
    }

    fieldsets = [
        (None, {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('awardee', 'start_date', 'end_date', 'allotment', 'description', 'scholarship_status', 'lateral', 'cleared'),
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

    suit_form_tabs = (('general', 'General'), ('thesis', 'Thesis / Dissertation Information'), 
        ('allocation', 'Scholarship Fund Allocations'), ('releases', 'Scholarship Fund Releases') )

    def get_readonly_fields (self, request, obj=None):
        if obj:
            return ('awardee',)
        else:
            return super(ScholarshipAdmin, self).get_readonly_fields(request, obj)

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