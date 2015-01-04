"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for University
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions, BooleanFieldListFilter
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, University, Department, Subject)

from django.http import HttpResponseRedirect
import threading
_thread_locals = threading.local()

class DepartmentInline(TabularInline):
    model = Department
    fk_name = 'university'
    extra = 0
    suit_classes = 'suit-tab suit-tab-department'

class SubjectInline(TabularInline):
    model = Subject
    verbose_name = 'Subject Offered'
    verbose_name_plural = 'Subjects Offered'
    fk_name = 'university'
    extra = 0
    suit_classes = 'suit-tab suit-tab-subject'

class UniversityAdmin(ERDTModelAdmin):
    list_display = ('name', 'address', 'landline_number')
    inlines = [DepartmentInline, SubjectInline]

    fieldsets = (
        (None, {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields' : ('photo', 'name', 'short_name', 'is_consortium', 'member_since', 'address', 
                'email_address', 'landline_number', 'no_semester', 'with_summer'),
        }),
    )

    suit_form_tabs = (('general', 'General'), ('department', 'Departments'), ('subject', 'Subjects Offered'))
    formfield_overrides = {
        models.ForeignKey: {'widget': LinkedSelect},
    }

    def get_fieldsets(self, request, obj=None):
        if not obj:
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)
                if my_profile.role == Profile.UNIV_ADMIN:
                    return (
                        (None, {
                            'classes' : ('suit-tab', 'suit-tab-general'),
                            'fields' : ('name', ),
                        }),
                    )
            except:
                pass
        return super(UniversityAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None):
        _thread_locals.request = request
        _thread_locals.obj = obj
        return super(UniversityAdmin, self).get_form(request, obj)

    def _suit_form_tabs(self):
        return self.get_suit_form_tabs(_thread_locals.request, _thread_locals.obj)

    suit_form_tabs = property(_suit_form_tabs)

    def get_suit_form_tabs(self, request, obj=None):
        if not obj:
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)
                if my_profile.role == Profile.UNIV_ADMIN:
                    return (('general', 'General'),)
            except:
                pass
        return (('general', 'General'), ('department', 'Departments'), ('subject', 'Subjects Offered'))


    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(UniversityAdmin, self).get_queryset(request)
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True) 

            if my_profile.role == Profile.UNIV_ADMIN: # If User's profile is CONSORTIUM
                return University.objects.filter(pk= my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return University.objects.filter(is_consortium=True)
        except Exception as e:
            print 'Error at UniversityAdmin', e
        return University.objects.none()
