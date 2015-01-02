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
from django.utils.html import format_html

# Import Profiling Module Models
from profiling.models import *

from django.http import HttpResponseRedirect


class GrantSummaryInline(TabularInline):
    model = Grant
    # template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'awardee'
    extra = 0
    verbose_name = 'Grant Awarded'
    verbose_name_plural = 'Grants Awarded'
    suit_classes = 'suit-tab suit-tab-grantsummary'
    exclude = ('description', 'delete')
    readonly_fields = ('grant_link', 'start_date', 'end_date', 'allotment', 'total_released', 'total_liquidated', 'balance')

class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    fk_name = 'payee'
    extra = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    exclude = ('description', 'grant', 'allocation')
    readonly_fields = ('release_link', 'date_released', 'amount_released', 'amount_liquidated', 'disparity')

class EquipmentIssuedInline(TabularInline):
    model = Equipment
    fk_name = 'payee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Issued Equipments'
    fields = ('description', 'status', 'accountable', 'date_released', 'surrendered')
    readonly_fields = fields

class EquipmentAccountableInline(TabularInline):
    model = Equipment
    fk_name = 'accountable'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Accountable Equipments'
    fields = ('issued_to', 'description', 'date_released',)
    readonly_fields = fields

    def issued_to(self, obj):
        return obj.payee

class ScholarshipInline(StackedInline):
    model = Scholarship
    fk_name = 'awardee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-scholarship'
    verbose_name = 'Local Scholarship'
    verbose_name_plural = 'Local Scholarships'
    fields = ('scholarship_status', 'degree_program', 'start_date', 'end_date' , 'allotment', 'adviser', 'entry_grad_program', 'end_grad_program', 'cleared' , 'description')
    readonly_fields = fields

class EquipmentInline(StackedInline):
    model = Equipment
    fk_name = 'payee'
    extra = 0
    suit_classes = 'suit-tab suit-tab-issued'

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     try:
    #         if db_field.name == 'grant':
    #             kwargs["queryset"] = Grant.objects.filter(awardee=resolve(request.path).args[0])
    #     except:
    #         pass
    #     return super(EquipmentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
    inlines = (ProfileInline, GrantSummaryInline, ReleaseInline, ScholarshipInline,
        EquipmentInline, EquipmentIssuedInline, EquipmentAccountableInline)
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

    #suit_form_tabs = (('general', 'General'), ('grantsummary', 'Grants Summary'),
     #   ('scholarship', 'Local Scholarships'), ('issued', 'Equipment'))

    formfield_overrides = {
        models.ForeignKey: {'widget': Select},
    }

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


                if is_student or is_faculty:
                    tabs.append(('grantsummary', 'Grants Summary'))
                    
                if is_student:
                    tabs.append(('scholarship', 'Local Scholarships'))

            except:
                print "error at get_suit_form_tabs ****************88"
                return tabs
            finally:
                return tabs
        return tabs

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting field-level permissions.
    Params: default
    Returns: default    
    """
    def get_readonly_fields(self, request, obj=None):
        try:
            profile = Profile.objectsself.get(person__user=request.user.id, active=True)
            if profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return self.readonly_fields + ('user', )
            else:
                return self.readonly_fields
        except Exception as e:
            print ("Error getting readonly fields: %s" % e.message)
            return self.readonly_fields

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True)

            if profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return qs.filter(user = request.user.id)
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                output_qs = set()
                user_person = Person.objects.get(user = request.user.id)
                output_qs.add(user_person.pk)
                for qs_person in qs:
                    for qs_profile in qs_person.profile_set.all():
                        if(qs_profile.university == profile.university):
                            output_qs.add(qs_person.pk)
                return qs.filter(pk__in = output_qs)
            else:
                return qs
        except:
            return qs
