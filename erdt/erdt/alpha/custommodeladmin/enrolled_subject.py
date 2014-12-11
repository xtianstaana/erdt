"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Enrolled Subject
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Enrolled_Subject)

from django.http import HttpResponseRedirect

class EnrolledSubjectAdmin(ERDTModelAdmin):
    list_filter = []
    readonly_fields = ()

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(EnrolledSubjectAdmin, self).get_queryset(request)
        
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.STUDENT: # If User's profile is STUDENT
                return qs.filter(scholarship__scholar__user = request.user.id)

            if profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                output_qs = set()

                thru_scholarship = Enrolled_Subject.objects.get(scholarship__high_degree_univ = profile.university)
                for p in thru_scholarship:
                    output_qs.add(p.pk)

                return qs.filter(pk__in = output_qs)

            else:
                return qs
        except:
            return qs