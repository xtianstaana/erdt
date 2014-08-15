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
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Item_Tag)

from django.http import HttpResponseRedirect

class DegreeProgramAdmin(ERDTModelAdmin):
    list_display = ('program', 'degree', 'department')
    list_filter = ('degree', 'department')

    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }

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
            profile = Profile.objects.get(person__user=request.user.id)
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is University Admin
                return qs.filter(department__university_id=profile.university.id)
            else:
                return qs
        except:
            return qs