"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Person
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Item_Tag)

from django.http import HttpResponseRedirect

class ProfileInline(TabularInline):
    model = Profile
    fk_name = 'person'
    exclude = ('active',)
    extra = 0

class ScholarshipInline(StackedInline):
    model = Scholarship
    fk_name = 'scholar'
    extra = 0
    max_num = 1

class PurchasedItemInline(TabularInline):
    model = Purchased_Item
    verbose_name = 'Issued Item'
    verbose_name_plural = 'Issued Items'
    fields = ['description', 'location', 'status', 'date_procured', 'accountable']
    fk_name = 'issuance'
    extra = 0

class AccountableInline(TabularInline):
    model = Purchased_Item
    verbose_name = 'Accountable Item'
    verbose_name_plural = 'Accountable Items'
    fields = ['description', 'location', 'status', 'date_procured']
    fk_name = 'accountable'
    extra = 0

class PersonAdmin(ERDTModelAdmin):
    inlines = [ProfileInline, ScholarshipInline, PurchasedItemInline, AccountableInline]
    list_display = ('__unicode__', 'email_address', 'mobile_number')
    readonly_fields = ('age',)
    list_filter = ('profile__role', 'profile__university', 'scholar__degree_program__degree', 'scholar__degree_program__program', 'scholar__scholarship_status')

    fieldsets = (
        ('Personal Information', {'fields': ('photo', 'user', 'first_name', 'middle_name', 'last_name', 'sex', 
            ('birthdate', 'age'), 'civil_status')}), 
        ('Contact Information', {'fields':('address', 'email_address', 'landline_number', 'mobile_number')}),
    )

    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting field-level permissions.
    Params: default
    Returns: default
    """
    def get_readonly_fields(self, request, obj=None):
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
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
