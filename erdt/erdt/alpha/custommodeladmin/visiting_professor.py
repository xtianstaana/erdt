from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *
from django.db.models import Q

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect
from django_select2.widgets import *

import threading
_thread_locals = threading.local()


class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    fk = 'grant'
    extra = 0
    max_num = 0
    fields =  ('release_link', 'date_released', 'amount_released', 'amount_liquidated', 'disparity')
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-releases'

    def has_delete_permission(self, request, obj=None):
        return False

class AllocationInline(TabularInline):
    model = Grant_Allocation
    fk_name = 'grant'
    extra = 0
    suit_classes = 'suit-tab suit-tab-allocation'

class MyVisitingProfessorForm(forms.ModelForm):
    class Meta:
        model = Visiting_Professor_Grant
        fields = '__all__'
        widgets = {
            'awardee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'host_university' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'host_professor' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class VisitingProfessorAdmin(ERDTModelAdmin):
    form = MyVisitingProfessorForm
    inlines =[AllocationInline, ReleaseInline]
    list_display = ('awardee', 'host_university', 'home_university')

    fieldsets = (
        (None, {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('awardee', 'description', 'start_date', 'end_date', 
                'allotment', 'distinguished', 'home_university', 'host_university', 'host_professor')
            }),
        (None, {
            'classes' : ('suit-tab', 'suit-tab-releases'),
            'fields' : ('allocation_summary',)
            }),
    )

    readonly_fields = ('allocation_summary',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'classes' : ('suit-tab', 'suit-tab-general'),
                    'fields' : ('awardee_link', 'description', 'start_date', 'end_date', 
                        'allotment', 'distinguished', 'home_university', 'host_university', 'host_professor')
                    }),
                (None, {
                    'classes' : ('suit-tab', 'suit-tab-releases'),
                    'fields' : ('allocation_summary',)
                    }),
            )            
        return super(VisitingProfessorAdmin, self).get_fieldsets(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'awardee':
                qs_t = Profile.objects.filter(role=Profile.VISITING)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs_t = qs_t.filter(university__pk=my_profile.university.pk)

                output_qs = tuple(p.person.pk for p in qs_t)
                kwargs["queryset"] = Person.objects.filter(pk__in=output_qs)
            elif db_field.name == 'host_university':
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
            elif db_field.name == 'host_professor':
                qs_t = Profile.objects.filter(role=Profile.ADVISER)

                if my_profile.role == Profile.UNIV_ADMIN:                    
                    qs_t = qs_t.filter(university__pk=my_profile.university.pk)
                    
                output_qs = tuple(p.person.pk for p in qs_t)
                kwargs["queryset"] = Person.objects.filter(pk__in=output_qs)
        except Exception as e:
            print '\n\n**************', e, '\n\n'
            kwargs["queryset"] = Person.objects.none()
        return super(VisitingProfessorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None):
        _thread_locals.request = request
        _thread_locals.obj = obj
        return super(VisitingProfessorAdmin, self).get_form(request, obj)

    def _suit_form_tabs(self):
        return self.get_suit_form_tabs(_thread_locals.request, _thread_locals.obj)

    suit_form_tabs = property(_suit_form_tabs)

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General'), ('allocation', 'Visiting Professor Grant Fund Allocations')]

        if obj:
            tabs.append(('releases', 'Release Summary'))
        return tabs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('awardee_link', 'allocation_summary')
        return super(VisitingProfessorAdmin, self).get_readonly_fields(request, obj)

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(VisitingProfessorAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is CONSORTIUM
                return Visiting_Professor_Grant.objects.filter(host_university__pk=profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Visiting_Professor_Grant.objects.all()
        except Exception as e:
            print 'Error at VisitingProfessorAdmin', e
        return Visiting_Professor_Grant.objects.none()
