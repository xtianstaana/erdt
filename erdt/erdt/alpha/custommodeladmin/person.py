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
    readonly_fields = ('grant_link', 'start_date', 'end_date', 'allotment', 'total_released', 'balance', 'is_active')

    def has_add_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'payee'
    extra = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    fields = ('date_released', 'release_link',  'amount_released', 'amount_liquidated', 'disparity')
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

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
    fields = ('date_released', 'property_no', 'description_link', 'status', 'accountable_link')
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
    fields = ('date_released', 'property_no', 'description_link', 'status', 'issued_to')
    readonly_fields = fields

    def issued_to(self, obj):
        return obj.payee

    def has_delete_permission(self, request, obj=None):
        return False

class ScholarshipInline(StackedInline):
    model = Scholarship
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-scholarship'
    fields = ('degree_program', 'scholarship_status', 'start_date', 'end_date', 'description', 'allotment', 'allocation_summary',
        'entry_grad_program', 'end_grad_program', 'ce_schedule',  'lateral', 'adviser', 'thesis_status', 'thesis_title',
        'thesis_topic', 'high_degree_univ', 'high_degree', 'cleared')
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class SandwichInline(StackedInline):
    model = Sandwich_Program
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-sandwich'

    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',
        'host_university', 'host_professor',)
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class Scholarship2Inline(StackedInline):
    model = ERDT_Scholarship_Special
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-scholarship'

    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',
        'host_university', 'host_professor',)
    readonly_fields = fields

    def has_delete_permission(self, request, obj=None):
        return False

class FRDGInline(StackedInline):
    model = FRDG
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',)
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-frdg'

    def has_delete_permission(self, request, obj=None):
        return False

class FRGTInline(StackedInline):
    model = FRGT
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',)
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-frgt'

    def has_delete_permission(self, request, obj=None):
        return False

class PostdocInline(StackedInline):
    model = Postdoctoral_Fellowship
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',)
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-postdoc'

    def has_delete_permission(self, request, obj=None):
        return False

class VisitingInline(StackedInline):
    model = Visiting_Professor_Grant
    fk_name = 'awardee'
    template = 'admin/edit_inline_with_link/stacked_with_link.html'
    extra = 0
    max_num = 0
    fields = ('start_date', 'end_date',  'description', 'allotment', 'allocation_summary',
        'distinguished', 'home_university', 'host_university', 'host_professor',)
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-visiting'

    def has_delete_permission(self, request, obj=None):
        return False

class AdviseesInline(TabularInline):
    model = Scholarship
    fk_name = 'adviser'
    verbose_name = 'Advisee'
    verbose_name_plural = 'Advisees'
    fields = ('awardee_link', 'degree_program', 'thesis_status', 'scholarship_status', 'end_date')
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-advisees'
    extra = 0
    max_num = 0

    def has_delete_permission(self, request, obj=None):
        return False

class EnrolledSubjectInline(TabularInline):
    model = Enrolled_Subject
    fk_name = 'scholar'
    extra = 0
    suit_classes = 'suit-tab suit-tab-enrolled'
    fields = ('subject', 'year_taken', 'eq_grade')

    def get_readonly_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role not in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return ('subject', 'year_taken', 'eq_grade')
        except:
            pass
        return super(EnrolledSubjectInline, self).get_readonly_fields(request, obj)

    def has_add_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

    def has_delete_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

class ProfileInline(TabularInline):
    model = Profile
    verbose_name_plural = 'Academic Profile'
    verbose_name_plural = 'Academic Profiles'
    exclude = ('active',)
    extra = 0
    suit_classes = 'suit-tab suit-tab-general'

    def get_readonly_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role not in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return ('role', 'university', )
        except:
            pass
        return super(ProfileInline, self).get_readonly_fields(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'university':
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
        except:
            pass
        return super(ProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

    def has_delete_permission(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return True
        except:
            pass
        return False

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)
                if my_profile.role == Profile.UNIV_ADMIN:                        
                    kwargs['choices'] = Profile.ADMIN_ROLE_CHOICES
            except Exception as e:
                print 'Error at ProfileInline', e
        return super(ProfileInline, self).formfield_for_choice_field(db_field, request, **kwargs)

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
    inlines = (ProfileInline, AdviseesInline, GrantSummaryInline, ReleaseInline, EquipmentIssuedInline, 
        EquipmentAccountableInline, Scholarship2Inline, ScholarshipInline, SandwichInline, 
        FRGTInline, FRDGInline, PostdocInline, VisitingInline, EnrolledSubjectInline)
    list_display = ('__unicode__', 'user', 'email_address', 'mobile_number')
    readonly_fields = ('age',)
    list_filter = ('profile__role', 'profile__university', )
    search_fields = ('first_name', 'last_name', 'middle_name', 'user__username')
    radio_fields =  {'sex' : HORIZONTAL, 'civil_status' : HORIZONTAL}
    fieldsets = (
        ('Personal Information', {
            'classes' : ('suit-tab', 'suit-tab-general',),
            'fields': ('photo', 'first_name', 'middle_name', 'last_name', 'sex', 'civil_status',
            ('birthdate', 'age'))
            }),
        ('Contact Information', {
            'classes' : ('suit-tab', 'suit-tab-general', 'collapse'),
            'fields':('address', 'address2', 'email_address', 'landline_number', 'mobile_number'),
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
                is_student_faculty = profiles.filter(Q(role=Profile.STUDENT)|Q(role=Profile.ADVISER)).exists()

                grants = Grant.objects.filter(awardee__pk=obj.pk)

                if Scholarship.objects.filter(adviser__pk=obj.pk):
                    tabs.append(('advisees', 'Advisees'), )

                if is_student_faculty:
                    tabs.append(('grantsummary', 'Grants Summary'))
                
                if grants.instance_of(Scholarship).exists() or grants.instance_of(ERDT_Scholarship_Special).exists():
                    tabs.append(('scholarship', 'Scholarships'))
                if grants.instance_of(Sandwich_Program).exists():
                    tabs.append(('sandwich', 'Sandwich Programs'))
                if grants.instance_of(FRGT).exists():
                    tabs.append(('frgt', 'FRGTs'))
                if grants.instance_of(FRDG).exists():
                    tabs.append(('frdg', 'FRDGs'))
                if grants.instance_of(Postdoctoral_Fellowship).exists():
                    tabs.append(('postdoc', 'Postdoctoral Fellowships'))
                if grants.instance_of(Visiting_Professor_Grant).exists():
                    tabs.append(('visiting', 'Visiting Professor Grants'))

                if grants.instance_of(Scholarship).exists():
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
                return Person.objects.filter(profile__university__pk=my_profile.university.pk).distinct()
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Person.objects.all()
        except Exception as e:
            print 'Error at PersonAdmin', e
        return Person.objects.none()
