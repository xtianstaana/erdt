"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Degree Program
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Department, Degree_Program)

from django.http import HttpResponseRedirect


class DegreeProgramAdmin(ERDTModelAdmin):
    list_display = ('program', 'degree', 'department', )
    list_filter = ('department__university', 'degree',)

    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }

    def get_readonly_fields (self, request, obj=None):
        if obj:
            return ('department',)
        else:
            return super(DegreeProgramAdmin, self).get_readonly_fields(request, obj)

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(DegreeProgramAdmin, self).get_queryset(request)

        try:
            profile = Profile.objects.get(person__user=request.user.id, active = True)
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is University Admin
                return qs.filter(department__university_id=profile.university.id)
            else:
                return qs
        except:
            return qs


    """
    Author: Christian Sta.Ana
    Date: Wed Oct 15 2014
    Description: Override the form on edit   
    Params: default
    Returns: default
    """            
    def render_change_form(self, request, context, *args, **kwargs):
        
        # For changing the choices of the Department Foreign Key
        dept_queryset = context['adminform'].form.fields["department"].queryset

        # Check current user's profile 
        try:
            profile = Profile.objects.get(person__user=request.user.id, active = True)
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is University Admin
                dept_queryset = Department.objects.filter(university_id = profile.university.id)
            else:
                print "Default view"
        except Exception as e:
            print("Error Getting Permissions: %s" % e.message)

        context['adminform'].form.fields["department"].queryset = dept_queryset
            
        
        return super(DegreeProgramAdmin, self).render_change_form(
            request, context, args, kwargs)

