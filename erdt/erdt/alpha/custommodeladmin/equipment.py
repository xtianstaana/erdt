"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Purchased Item
"""

from globals import ERDTModelAdmin
from profiling.models import *
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget
from django_select2.widgets import Select2Widget
from django.forms import ModelForm
from django.http import HttpResponse
import csv

class MyEquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'payee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'description' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'amount_released' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
            'amount_liquidated' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
            'date_released' : SuitDateWidget,
            'accountable' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class PurchasedItemAdmin(ERDTModelAdmin):
    form = MyEquipmentForm

    list_display = (
        'date_released', 'property_no', 'description_link', 'payee_sub', 'university')
    list_display_links = None
    search_fields = ('property_no', 'description', 'university__name', 'university__short_name')
    exclude = ('item_type',)

    list_filter = ('university', 'status', 'surrendered', )
    actions = ('export_csv',)
    list_max_show_all = 10000000

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="equipment_list.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ERDT Equipment List'])
        writer.writerow([])
        writer.writerow(
            ['Payee', 'Funding Grant', 'Date Released', 'Amount Released', 'Amount Liquidated', 
             'Description', 'Property no.', 'University', 'Location', 'Status',
             'Accountable', 'Donated']
        )
        for q in queryset:
            e = Equipment.objects.get(pk=q.pk)

            write = [
                e.payee.__str__(),
                e.allocation.__str__(),
                e.date_released.__str__(),
                e.amount_released,
                e.amount_liquidated,
                e.description,
                e.property_no,
                e.university.__str__(),
                e.location,
                e.get_status_display(),
                e.accountable.__str__(),
                e.surrendered
                ]
            writer.writerow(write)
        return response

    export_csv.short_description = 'Export selected Equipment to CSV'

    def grant_link(self, obj=None):
        return obj.grant.grant_link()
    grant_link.short_description = 'Funding grant'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                is_person = 1
                qs = Person.objects.filter(grants__isnull=False)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'accountable':
                is_person = 1
                qs = Person.objects.filter(profile__role=Profile.ADVISER)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'university':
                is_person = 2
                qs = University.objects.filter(is_consortium=True)
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
        except:
            if is_person == 1:
                kwargs["queryset"] = Person.objects.none()
            elif is_person == 2:
                kwargs["queryset"] = University.objects.none()
        return super(PurchasedItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        payee = 'payee'
        grant = 'grant'
        if obj:
            payee = 'payee_link'
            grant = 'grant_link'
        return (
            (None, {
                'fields' : (payee, grant, 'allocation', 'date_released', 'amount_released', 
                    'amount_liquidated', 'description',)
                }),
            ('Other Information', {
                'fields' : ('property_no', 'university', 'location',  'status', 'accountable', 'surrendered', )
                }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation', 'grant_link')
        else:
            return super(PurchasedItemAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if  my_profile.role == Profile.UNIV_ADMIN:
                return Equipment.objects.filter(
                    university=my_profile.university.id)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Equipment.objects.all()
        except Exception as e:
            print 'Error', e
        return Equipment.objects.none()