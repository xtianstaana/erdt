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
from django_select2.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Equipment, Enrolled_Subject)

from django.http import HttpResponseRedirect


class MyEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'payee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'accountable' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class PurchasedItemAdmin(ERDTModelAdmin):
    form = MyEquipmentForm

    list_display = ('date_released', 'particular', 'payee', 'accountable', 'surrendered')
    exclude = ('item_type',)

    list_filter = ('surrendered',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'fields' : ('payee_link', 'allocation', 'description', 'amount_released', 
                'amount_liquidated', 'date_released', )
                    }),
                ('Other Information', {
                    'fields' : ('location', 'property_no', 'status', 'surrendered', 'accountable')
                    }),
            )
        return (
            (None, {
                'fields' : ('payee', 'grant', 'allocation', 'description', 'amount_released', 
            'amount_liquidated', 'date_released', )
                }),
            ('Other Information', {
                'fields' : ('location', 'property_no', 'status', 'surrendered', 'accountable')
                }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation', )
        else:
            return super(PurchasedItemAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super(PurchasedItemAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 

            if profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                output_qs = set()
                
                thru_issuance = Equipment.objects.get(payee__user = request.user.id)
                for p in thru_issuance:
                    output_qs.add(p.pk)
                
                thru_accountable = Equipment.objects.get(accountable__user = request.user.id)
                for p in thru_accountable:
                    output_qs.add(p.pk)


                return qs.filter(pk__in = output_qs)
            else:
                return qs
        except:
            return qs