"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for User 
"""

from globals import ERDTModelAdmin
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Item_Tag)

from django.http import HttpResponseRedirect

class UserForm(ModelForm):
    class Meta:
        widgets = {
            'password': PasswordInput()
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UserAdmin(ERDTModelAdmin):

    fieldsets = [
        ('Authentication', {'fields': ['username', 'password', 'email']}),
        ('Advanced Information', {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'user_permissions'],
            'classes': ['collapse', 'wide'],
            })
    ]

    form = UserForm

