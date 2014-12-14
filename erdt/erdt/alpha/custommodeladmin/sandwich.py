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
from profiling.models import (Profile, University, Sandwich_Program, Grant_Allocation)

from django.http import HttpResponseRedirect


class AllocationInline(TabularInline):
    model = Grant_Allocation
    fk_name = 'grant'
    extra = 0

class SandwichAdmin(ERDTModelAdmin):
    inlines =[AllocationInline]
    list_display = ('year', 'awardee', 'host_university')

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(SandwichAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is CONSORTIUM
                return qs.filter(profile__university__id = profile.university.id)
            else:
                return qs
        except:
            return qs
