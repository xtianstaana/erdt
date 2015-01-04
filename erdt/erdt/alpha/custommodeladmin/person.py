"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Person
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions, HORIZONTAL, VERTICAL
from django.contrib.admin.options import InlineModelAdmin
from django import forms
from django.forms.widgets import *
from suit.widgets import *
from django.core.urlresolvers import resolve, reverse
from django_select2.widgets import *
from django.utils.translation import ugettext_lazy as _

# Import Profiling Module Models
from profiling.models import *

from django.http import HttpResponseRedirect


class GrantSummaryInline(TabularInline):
    model = Grant
    template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'awardee'
    extra = 0
    verbose_name = 'Grant Awarded'
    verbose_name_plural = 'Grants Awarded'
    suit_classes = 'suit-tab suit-tab-grantsummary'
    exclude = ('description', 'delete')
    readonly_fields = ('grant_link', 'start_date', 'end_date', 'allotment', 'total_liquidated', 'balance', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False

class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'payee'
    extra = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    fields = ('release_link', 'date_released', 'amount_released', 'amount_liquidated', 'disparity')
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class EquipmentIssuedInline(TabularInline):
    model = Equipment
    fk_name = 'payee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Issued Equipments'
    fields = ('description_link', 'status', 'accountable_link', 'date_released', 'surrendered')
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class EquipmentAccountableInline(TabularInline):
    model = Equipment
    fk_name = 'accountable'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Accountable Equipments'
    fields = ('issued_to', 'description_link', 'date_released',)
    readonly_fields = fields

    def issued_to(self, obj):
        return obj.payee

    def has_delete_permission(self, request, obj=None):
        return False

class ScholarshipInline(StackedInline):
    model = Scholarship
    fk_name = 'awardee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-scholarship'
    verbose_name = 'Local Scholarship'
    verbose_name_plural = 'Local Scholarships'
    fields = ('scholarship_status', 'degree_program',  'adviser', 'thesis_status', 'start_date', 'end_date', 
        'entry_grad_program', 'end_grad_program', 'description', 'lateral', 'cleared' , 'allotment', 
        'allocation_summary',)
    readonly_fields = fields

    def __unicode__(self, obj=None):
        if obj:
            return self.grant_link()

    def has_delete_permission(self, request, obj=None):
        return False

class SandwichInline(StackedInline):
    model = Sandwich_Program
    fk_name = 'awardee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-sandwich'

    fields = ('start_date', 'end_date', 'host_university', 'host_professor', 'description', 'allotment', 
        'allocation_summary')
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class EnrolledSubjectInline(TabularInline):
    model = Enrolled_Subject
    fk_name = 'scholar'
    extra = 0
    suit_classes = 'suit-tab suit-tab-enrolled'
    fields = ('subject', 'year_taken', 'eq_grade')

class ProfileInline(TabularInline):
    model = Profile
    verbose_name_plural = 'Academic Profile'
    verbose_name_plural = 'Academic Profiles'
    exclude = ('active',)
    extra = 0
    suit_classes = 'suit-tab suit-tab-general'

class MyPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'user' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

import threading
_thread_locals = threading.local()

class PersonAdmin(ERDTModelAdmin):
    form = MyPersonForm
    inlines = (ProfileInline, GrantSummaryInline, EquipmentIssuedInline, 
        EquipmentAccountableInline, ReleaseInline, ScholarshipInline, SandwichInline, EnrolledSubjectInline)
    list_display = ('__unicode__', 'email_address', 'mobile_number')
    readonly_fields = ('age',)
    list_filter = ('profile__role', 'profile__university', 'awardee__scholarship__degree_program__degree',
        'awardee__scholarship__degree_program__program', 'awardee__scholarship__scholarship_status')
    radio_fields =  {'sex' : HORIZONTAL, 'civil_status' : HORIZONTAL}
    fieldsets = (
        ('Personal Information', {
            'classes' : ('suit-tab', 'suit-tab-general',),
            'fields': ('photo', 'first_name', 'middle_name', 'last_name', 'sex', 'civil_status',
            ('birthdate', 'age'))
            }),
        ('Contact Information', {
            'classes' : ('suit-tab', 'suit-tab-general', 'collapse'),
            'fields':('address', 'email_address', 'landline_number', 'mobile_number'),
            }),
        ('User Account', {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields':('user', ),
            }),
    )

    def get_form(self, request, obj=None):
        _thread_locals.request = request
        _thread_locals.obj = obj
        return super(PersonAdmin, self).get_form(request, obj)

    def _suit_form_tabs(self):
        return self.get_suit_form_tabs(_thread_locals.request, _thread_locals.obj)

    suit_form_tabs = property(_suit_form_tabs)

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General')]
        if obj:
            try:
                profiles = Profile.objects.filter(person__pk=obj.pk)
                is_student = profiles.filter(role=Profile.STUDENT).count() > 0
                is_faculty =  profiles.filter(role=Profile.ADVISER).count() > 0

                grants = Grant.objects.filter(awardee__pk=obj.pk)


                if is_student or is_faculty:
                    tabs.append(('grantsummary', 'Grants Summary'))
                    
                if grants.instance_of(Scholarship):
                    tabs.append(('scholarship', 'Local Scholarships'))
                if grants.instance_of(ERDT_Scholarship_Special):
                    tabs.append(('sscholarship', 'Abroad Scholarships'))
                if grants.instance_of(Sandwich_Program):
                    tabs.append(('sandwich', 'Sandwich Programs'))
                if grants.instance_of(Postdoctoral_Fellowship):
                    tabs.append(('postdoc', 'Postdoctoral Fellowships'))
                if grants.instance_of(FRGT):
                    tabs.append(('frgt', 'FRGT'))
                if grants.instance_of(FRDG):
                    tabs.append(('frdg', 'FRDG'))

                if grants.instance_of(Scholarship):
                    tabs.append(('enrolled', 'Enrolled Subjects'))
            except:
                pass
        return tabs
    
    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)

            if my_profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return Person.objects.filter(user__pk=request.user.pk)
            elif my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                return Person.objects.filter(profile__university__pk=my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Person.objects.all()
        except Exception as e:
            print 'Error at PersonAdmin', e
        return Person.objects.none()
