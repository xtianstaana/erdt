"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Person
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions, HORIZONTAL, VERTICAL
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Grant)

from django.http import HttpResponseRedirect

class ProfileInline(TabularInline):
    model = Profile
    exclude = ('active',)
    extra = 0
    suit_classes = 'suit-tab suit-tab-profile'

class GrantInline(TabularInline):
    model = Grant
    fk_name = 'recipient'
    extra = 0
    suit_classes = 'suit-tab suit-tab-grant'

class ScholarshipInline(StackedInline):
    model = Scholarship
    fk_name = 'recipient'
    extra = 0
    suit_classes = 'suit-tab suit-tab-scholarship'


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'first_name' : TextInput(attrs={'placeholder':'First name'}),
            'middle_name' : TextInput(attrs={'placeholder':'Middle name'}),
            'last_name' : TextInput(attrs={'placeholder':'Last name'}),
        }

class PersonAdmin(ERDTModelAdmin):
    form = PersonForm
    inlines = [ProfileInline, GrantInline]
    list_display = ('__unicode__', 'email_address', 'mobile_number')
    readonly_fields = ('age',)
    list_filter = ('profile__role', 'profile__university', 'grant_recipient__scholarship__degree_program__degree', 'grant_recipient__scholarship__degree_program__program', 'grant_recipient__scholarship__scholarship_status')
    radio_fields =  {'sex' : HORIZONTAL, 'civil_status' : HORIZONTAL}

    fieldsets = (
        ('Personal Information', {
            'classes' : ('suit-tab', 'suit-tab-information'),
            'fields': ('photo', 'user', 'first_name', 'middle_name', 'last_name', 'sex', 'civil_status',
            ('birthdate', 'age'))
            }), 
        ('Contact Information', {
            'classes' : ('suit-tab', 'suit-tab-information'),
            'fields':('address', 'email_address', 'landline_number', 'mobile_number'), 
            }),
    )

    suit_form_tabs = (('information', 'Information'), ('profile', 'Profiles'), ('grant', 'Grants'))

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
            #print ("Error getting readonly fields: %s" % e.message)
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
