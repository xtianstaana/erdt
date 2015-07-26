"Filter queryset for UNIV_ADMIN. What type of fund releases are they capable of? Sandwich?"

from globals import ERDTModelAdmin
from profiling.models import *
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget
from django_select2.widgets import Select2Widget
from django.forms import ModelForm

class MyGrantAllocationReleaseForm(ModelForm):
    class Meta:
        model = Grant_Allocation_Release
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
        }

class GrantAllocationReleaseAdmin(ERDTModelAdmin):
    form = MyGrantAllocationReleaseForm
    model = Grant_Allocation_Release
    list_display = ('date_released', 'release_link', 'payee_sub', )
    list_display_links = None
    list_filter = ('item_type',)
    search_fields = ('payee__first_name', 'payee__last_name', 'payee__middle_name', 'description')

    def grant_link(self, obj=None):
        return obj.grant.grant_link()
    grant_link.short_description = 'Funding grant'

    def get_fields(self, request, obj=None):
        if obj:
            if obj.item_type == '':
                return ('payee_link', 'grant_link', 'allocation', 'date_released','amount_released', 'amount_liquidated', 'description',)
            else:
                return ('payee_link', 'grant_link', 'allocation', 'date_released','amount_released', 'amount_liquidated', 'item_type', 'description',)
        return ('payee', 'grant', 'allocation', 'date_released', 'amount_released', 'amount_liquidated', 'item_type', 'description',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'payee':
                qs = Person.objects.filter(grants__isnull=False)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__id=my_profile.university.id)
                kwargs["queryset"] = qs.distinct()
        except Exception as e:
            kwargs["queryset"] = Person.objects.none()
        return super(GrantAllocationReleaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'item_type':
                kwargs['choices'] = ((u'', '-'*10),) + Grant_Allocation_Release.ITEMTYPE_CHOICES
        return super(GrantAllocationReleaseAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.__class__ in (Equipment, Research_Dissemination):
                return ('payee_link', 'allocation', 'item_type', 'grant_link')
            return ('payee_link', 'allocation', 'grant_link')
        return super(GrantAllocationReleaseAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if  my_profile.role == Profile.UNIV_ADMIN:
                return Grant_Allocation_Release.objects.filter(
                    grant__record_manager__id=my_profile.university.id).distinct()
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Grant_Allocation_Release.objects.all()
        except Exception as e:
            print 'Error', e
        return Grant_Allocation_Release.objects.none()