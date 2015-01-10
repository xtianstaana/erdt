"Filter queryset for UNIV_ADMIN. What type of fund releases are they capable of? Sandwich?"

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


class MyGrantAllocationReleaseForm(forms.ModelForm):
    class Meta:
        model = Grant_Allocation_Release
        fields = '__all__'
        widgets = {
            'payee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class GrantAllocationReleaseAdmin(ERDTModelAdmin):
    form = MyGrantAllocationReleaseForm
    model = Grant_Allocation_Release
    list_display = ('date_released', 'release_link', 'payee_sub', 'item_type', )
    list_display_links = None
    list_filter = ('item_type',)

    def get_fields(self, request, obj=None):
        if obj:
            return ('payee_link', 'allocation', 'description', 'item_type', 'amount_released', 'amount_liquidated', 'date_released',)
        return ('payee', 'grant', 'allocation', 'description' ,'item_type', 'amount_released', 'amount_liquidated', 'date_released', )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                qs = Person.objects.filter(profile__role__in=(Profile.ADVISER, Profile.STUDENT, Profile.VISITING))
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'item_type':
                kwargs['choices'] = ((u'', '-'*10),) + Grant_Allocation_Release.ITEMTYPE_CHOICES
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(GrantAllocationReleaseAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.__class__ in (Equipment, Research_Dissemination):
                return ('payee_link', 'allocation', 'item_type')
            return ('payee_link', 'allocation')
        return super(GrantAllocationReleaseAdmin, self).get_readonly_fields(request, obj)