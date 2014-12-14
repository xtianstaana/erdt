"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Grant Allocation Release
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect

class GrantAllocationReleaseAdmin(ERDTModelAdmin):
    model = Grant_Allocation_Release
    ordering = ('-date_released', 'payee')
    list_display = ['date_released', 'the_who', 'particular' ]
