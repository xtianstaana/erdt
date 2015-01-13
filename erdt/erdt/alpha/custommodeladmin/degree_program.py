"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Degree Program
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
from django_select2.widgets import *


class MyDegreeProgramForm(ModelForm):
    class Meta:
        model = Degree_Program
        fields = '__all__'
        widgets = {
            'department' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class DegreeProgramAdmin(ERDTModelAdmin):
    form = MyDegreeProgramForm
    list_display = ('program', 'degree', 'department', )
    list_filter = ('department__university', 'degree',)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            if db_field.name == 'department':
                my_profile = Profile.objects.get(person__user=request.user.id, active = True)

                kwargs["queryset"] = Department.objects.filter(university__pk = my_profile.university.pk).distinct()
        except:
            pass
        return super(DegreeProgramAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    """
    Author: Christian Sta.Ana
    Date: Mon Aug 11 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(DegreeProgramAdmin, self).get_queryset(request)

        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active = True)
            if my_profile.role == Profile.UNIV_ADMIN:
                return qs.filter(department__university_id=my_profile.university.id)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Degree_Program.objects.all()
        except Exception as e:
            print 'Error at DegreeProgramAdmin', e
        return Degree_Program.objects.none()