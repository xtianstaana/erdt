"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for University
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject)

from django.http import HttpResponseRedirect

class DepartmentInline(TabularInline):
    model = Department
    fk_name = 'university'
    extra = 0
    suit_classes = 'suit-tab suit-tab-department'

class SubjectInline(TabularInline):
    model = Subject
    verbose_name = 'Subject Offered'
    verbose_name_plural = 'Subjects Offered'
    fk_name = 'university'
    extra = 0
    suit_classes = 'suit-tab suit-tab-subject'

class UniversityAdmin(ERDTModelAdmin):
    list_display = ('name', 'is_consortium', 'address')
    list_filter = ('is_consortium',)
    inlines = [DepartmentInline, SubjectInline]

    fieldsets = [
        (None, {
            'classes' : ('suit-tab', 'suit-tab-information'),
            'fields' : ('photo', 'name', 'is_consortium', 'member_since', 'address', 'email_address', 'landline_number', 'no_semester', 'with_summer'),
            }),
    ]

    suit_form_tabs = (('information', 'Information'), ('department', 'Departments'), ('subject', 'Subjects Offered'))
    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(UniversityAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is CONSORTIUM
                return qs.filter(pk = profile.university.id)
            else:
                return qs
        except:
            return qs
