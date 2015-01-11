from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *
from django.db.models import Q

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect
from django_select2.widgets import *

import threading
_thread_locals = threading.local()


class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    fk = 'grant'
    extra = 0
    max_num = 0
    fields =  ('release_link', 'date_released', 'amount_released', 'amount_liquidated', 'disparity')
    readonly_fields = fields
    suit_classes = 'suit-tab suit-tab-releases'

    def has_delete_permission(self, request, obj=None):
        return False

class AllocationInline(TabularInline):
    model = Grant_Allocation
    fk_name = 'grant'
    extra = 0
    max_num = 1
    suit_classes = 'suit-tab suit-tab-allocation'
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['choices'] = Grant_Allocation.POSTDOCTORAL_ALLOC_CHOICES
        return super(AllocationInline, self).formfield_for_choice_field(db_field, request, **kwargs)

class MyForm(forms.ModelForm):
    class Meta:
        model = Postdoctoral_Fellowship
        fields = '__all__'
        widgets = {
            'awardee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class PostdoctoralAdmin(ERDTModelAdmin):
    form = MyForm
    inlines =[AllocationInline, ReleaseInline]
    list_display = ('awardee', 'start_date', 'end_date', )

    fieldsets = [
        (None, {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('awardee', 'description', 'start_date', 'end_date', 
                'allotment',)
            }),
        (None, {
            'classes' : ('suit-tab', 'suit-tab-releases'),
            'fields' : ('allocation_summary',)
            }),
    ]

    readonly_fields = ('allocation_summary',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [
                (None, {
                    'classes' : ('suit-tab', 'suit-tab-general'),
                    'fields' : ('awardee_link', 'description', 'start_date', 'end_date', 
                        'allotment',)
                    }),
                (None, {
                    'classes' : ('suit-tab', 'suit-tab-releases'),
                    'fields' : ('allocation_summary',)
                    }),
            ]            
        return super(PostdoctoralAdmin, self).get_fieldsets(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'awardee':
                qs = Person.objects.filter(profile__role=Profile.ADVISER)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(PostdoctoralAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None):
        _thread_locals.request = request
        _thread_locals.obj = obj
        return super(PostdoctoralAdmin, self).get_form(request, obj)

    def _suit_form_tabs(self):
        return self.get_suit_form_tabs(_thread_locals.request, _thread_locals.obj)

    suit_form_tabs = property(_suit_form_tabs)

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General'), ('allocation', 'Postdoctoral Fellowship Fund Allocations')]

        if obj:
            tabs.append(('releases', 'Release Summary'))
        return tabs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('awardee_link', 'allocation_summary')
        return super(PostdoctoralAdmin, self).get_readonly_fields(request, obj)
