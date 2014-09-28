"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Purchased Item
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

class PurchasedItemAdmin(ERDTModelAdmin):
    readonly_fields = ()

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(PurchasedItemAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 

            if profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                output_qs = set()
                
                thru_issuance = Purchased_Item.objects.get(issuance__user = request.user.id)
                for p in thru_issuance:
                    output_qs.add(p.pk)
                
                thru_accountable = Purchased_Item.objects.get(accountable__user = request.user.id)
                for p in thru_accountable:
                    output_qs.add(p.pk)

                thru_fundsource = Purchased_Item.objects.get(fund_source__high_degree_univ = profile.university)
                for p in thru_fundsource:
                    output_qs.add(p.pk)

                return qs.filter(pk__in = output_qs)
            else:
                return qs
        except:
            return qs