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

    list_display = ('date_released', 'particular', 'payee_sub', 'accountable_univ', 'surrendered')
    list_display_links = ('particular', )
    exclude = ('item_type',)

    list_filter = ('surrendered',)

    def accountable_univ(self, obj=None):
        try:
            if obj:
                p = Profile.objects.get(person__pk=obj.accountable.pk, role=Profile.ADVISER)
                return '%s / %s' % (obj.accountable_sub(), p.university.short_name)
        except:
            pass
        return 'Unknown'
    accountable_univ.short_description = 'Accountable'
    accountable_univ.admin_order_field = 'accountable'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                qs = Person.objects.filter(profile__role__in=(Profile.ADVISER, Profile.STUDENT))
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'accountable':
                qs = Person.objects.filter(profile__role=Profile.ADVISER)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(PurchasedItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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