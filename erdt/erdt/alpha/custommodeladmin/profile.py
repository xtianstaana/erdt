"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Profile
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

class ProfileAdmin(ERDTModelAdmin):
    list_display = ('person', 'role', 'affiliation', 'active') 
    list_filter = ('role',)

    fieldsets = [
        ('Details', {'fields': ['active' ,'role','person']}),
        ('Affiliation', {'fields': ['university']})
    ]

    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }
