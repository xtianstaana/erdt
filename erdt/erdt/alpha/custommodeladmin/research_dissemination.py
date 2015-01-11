"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Research Dissemination
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
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django_select2.widgets import *


class MyResearchDisseminationForm(forms.ModelForm):
    class Meta:
        model = Research_Dissemination
        fields = '__all__'
        widgets = {
            'payee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class ResearchDisseminationAdmin(ERDTModelAdmin):
    form = MyResearchDisseminationForm
    list_display = ('date_released', 'particular', 'payee_sub', 'paper_title',)
    list_display_links = ('paper_title',)
    exclude = ('item_type',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                qs = Person.objects.filter(profile__role__in=(Profile.ADVISER, Profile.STUDENT))
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(ResearchDisseminationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'fields' : ('payee_link', 'allocation', 'description', 'amount_released', 
                'amount_liquidated', 'date_released', )
                    }),
                ('Other Information', {
                    'fields' : (('paper_title', 'conference_name', 'conference_loc', 'conference_date'))
                    }),
            )
        return (
            (None, {
                'fields' : ('payee', 'grant', 'allocation', 'description', 'amount_released', 
            'amount_liquidated', 'date_released', )
                }),
            ('Other Information', {
                'fields' : (('paper_title', 'conference_name', 'conference_loc', 'conference_date'))
                }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation')
        return super(ResearchDisseminationAdmin, self).get_readonly_fields(request, obj)