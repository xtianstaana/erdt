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
    extra = 0
    suit_classes = 'suit-tab suit-tab-allocation'

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['choices'] = Grant_Allocation.SCHOLARSHIP_ALLOC_CHOICES
        return super(AllocationInline, self).formfield_for_choice_field(db_field, request, **kwargs)

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
            'high_degree_univ' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class ScholarshipAdmin(ERDTModelAdmin):
    form = MyScholarshipForm
    inlines = [AllocationInline, ReleaseInline]
    list_display = ('awardee', 'degree_program', 'start_date', 'adviser')
    list_filter = ('degree_program__department__university__name', 'degree_program', 'start_date','scholarship_status')

    readonly_fields = ('allocation_summary',)

    def get_fieldsets(self, request, obj=None):
        _fieldsets =  (
            ('Program Details', {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('university', 'degree_program', 'entry_grad_program' , 'end_grad_program', 'ce_schedule'),
                }),
            ('Educational Background', {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('high_degree_univ', 'high_degree'),
                }),
            (None, {
                'classes' : ('suit-tab', 'suit-tab-thesis'),
                'fields' : ('adviser', 'thesis_status', 'thesis_title', 'thesis_topic'),
                }),
            (None, {
                'classes' : ('suit-tab', 'suit-tab-releases'),
                'fields' : ('allocation_summary',)
                }),
        )
        if obj:
            return ((None, {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('awardee_link', 'start_date', 'end_date', 'allotment', 'description', 'scholarship_status', 'lateral', 'cleared'),
                }),) + _fieldsets
        return ((None, {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('awardee', 'start_date', 'end_date', 'allotment', 'description', 'scholarship_status', 'lateral', 'cleared'),
                }),) + _fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('awardee_link', 'allocation_summary')
        return super(ScholarshipAdmin, self).get_readonly_fields(request, obj)

    def get_form(self, request, obj=None):
        _thread_locals.request = request
        _thread_locals.obj = obj
        return super(ScholarshipAdmin, self).get_form(request, obj)

    def _suit_form_tabs(self):
        return self.get_suit_form_tabs(_thread_locals.request, _thread_locals.obj)

    suit_form_tabs = property(_suit_form_tabs)

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General'), ('thesis', 'Thesis / Dissertation Information'), 
        ('allocation', 'Scholarship Fund Allocations')]

        if obj:
            tabs.append(('releases', 'Release Summary'))
        return tabs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'awardee':
                qs = Person.objects.filter(profile__role=Profile.STUDENT)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'university':
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
            elif db_field.name == 'adviser':
                qs = Person.objects.filter(profile__role=Profile.ADVISER)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(ScholarshipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)

            if my_profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return Scholarship.objects.filter(awardee__pk=my_profile.person.pk).distinct()
            elif my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                return Scholarship.objects.filter(university__pk=my_profile.university.pk).distinct()
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Scholarship.objects.all()
        except Exception as e:
            print 'Error at ScholarshipAdmin', e
        return Scholarship.objects.none()