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
from profiling.models import (Profile, Person)
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

    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.      
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        try:
            profile = Profile.objects.get(person__user=request.user.id, active=True) 
            if profile.role == Profile.UNIV_ADMIN: # If User's profile is CONSORTIUM
                
                # Get each user's person record 
                output_qs = set()
                for qs_user in qs:
                    try:
                        userPerson = Person.objects.get(user = qs_user.pk)
                        for userProfile in userPerson.profile_set.all():
                            if(userProfile.university == profile.university):
                                output_qs.add(qs_user.pk)
                    except:
                        print 'Error getting a person in user queryset'

                return qs.filter(pk__in = output_qs)
            else:
                return qs
        except:
            return qs

