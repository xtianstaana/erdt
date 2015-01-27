"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Research Dissemination
"""

from globals import ERDTModelAdmin
from profiling.models import *
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget
from django_select2.widgets import Select2Widget
from django.forms import ModelForm

class MyResearchDisseminationForm(ModelForm):
    class Meta:
        model = Research_Dissemination
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
            'conference_date' : SuitDateWidget,
        }

class ResearchDisseminationAdmin(ERDTModelAdmin):
    form = MyResearchDisseminationForm
    list_display = ('date_released', 'release_link', 'payee_sub', 'paper_title',)
    list_display_links = None
    search_fields = ('payee__first_name', 'payee__last_name', 'payee__middle_name', )
    exclude = ('item_type',)
    
    def grant_link(self, obj=None):
        return obj.grant.grant_link()
    grant_link.short_description = 'Funding grant'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                qs = Person.objects.filter(grants__isnull=False)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(ResearchDisseminationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
                'fields' : (('paper_title', 'conference_name', 'conference_loc', 'conference_date'))
                }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation', 'grant_link')
        return super(ResearchDisseminationAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if  my_profile.role == Profile.UNIV_ADMIN:
                return Research_Dissemination.objects.filter(
                    grant__record_manager__id=my_profile.university.id).distinct()
            elif my_profile.role == Profile.CENTRAL_OFFICE:
                return Research_Dissemination.objects.all()
        except Exception as e:
            print 'Error', e
        return Research_Dissemination.objects.none()