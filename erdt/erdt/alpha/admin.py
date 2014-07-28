"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains Admin Customization functions
"""

import sys

from django.contrib.admin import AdminSite
from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline, actions
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.contenttypes import views as contenttype_views
from django.views.decorators.csrf import csrf_protect
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.forms.models import model_to_dict

# Utility methods
from views import turn_form_friendly

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item)

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Overrides the default Django AdminSite object
"""
class ERDTAdminSite(AdminSite):

    """
    Author: Christian Sta.Ana
    Date: Wed Jul 23 2014
    Description: Overrides the index view of the AdminSite
    Params: default
    Returns: default
    Revisions:
    07/26/14 - Retrieval of profile and person data added
    """
    @never_cache
    def index(self, request, extra_context=None):
        erdtIndexTempRes = super(ERDTAdminSite, self).index(request)

        erdtIndexTempRes.context_data['title'] = constants['constants']['site']['index_title']
        
        # get current user data
        currentUser = request.user

        currentUserProfile = None
        currentUserPerson = None
        userFields = None
        personFields = None

        try:
            currentUserProfile = Profile.objects.get(user = currentUser.id)
            currentUserPerson = Person.objects.get(id = currentUserProfile.person.id)
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)

        #excluded fields list
        user_exclude = ['first_name', 'last_name', 'is_active', 'email', 'is_superuser', 'is_staff', 'groups', 
            'password', 'id', 'date_joined', 'user_permissions']
        person_exclude = ['photo', 'id']

        if(currentUser):
            userFields = turn_form_friendly(model_to_dict(currentUser), user_exclude, {})

        if(currentUserPerson):
            personFields = turn_form_friendly(model_to_dict(currentUserPerson), person_exclude, {})

        erdtIndexTempRes.context_data['current_user'] = currentUser
        erdtIndexTempRes.context_data['current_user_profile'] = currentUserProfile
        erdtIndexTempRes.context_data['current_user_person'] = currentUserPerson

        erdtIndexTempRes.context_data['user_fields'] = userFields
        erdtIndexTempRes.context_data['person_fields'] = personFields

        return erdtIndexTempRes

class UserAdmin(ModelAdmin):

    fieldsets = [
        ('Authentication', {'fields': ['username', 'password', 'email']}),
        ('Advanced Information', {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'user_permissions'],
            'classes': ['collapse',],
            })
    ]

class ProfileAdmin(ModelAdmin):
    list_display = ('person', 'role') 
    list_filter = ('role',)

    fieldsets = [
        ('Details', {'fields': ['role', 'user', 'person']}),
        ('School Information', {'fields': ['university', 'department', 'scholarship']})
    ]

class DegreeProgramAdmin(ModelAdmin):
    list_display = ('program', 'degree', 'department')
    list_filter = ('degree', 'department__university__name')

class DepartmentAdmin(ModelAdmin):
    list_display = ('name', 'university',)
    list_filter = ('university',)

class PersonAdmin(ModelAdmin):
    list_display = ('__unicode__', 'email_address', 'mobile_number')
    search_fields = ('first_name', 'middle_name', 'last_name')

class SubjectAdmin(ModelAdmin):
    list_display = ('course_title', 'course_units', 'university')
    list_filter = ('university',)

class UniversityAdmin(ModelAdmin):
    list_display = ('name', 'no_semester', 'with_summer', 'email_address', 'landline_number')

# Set the admin_site object as the custom ERDT Admin Site
admin_site = ERDTAdminSite()

# Register Django models
admin_site.register(User, UserAdmin)

# Register Profiling models
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Person, PersonAdmin) 
admin_site.register(University, UniversityAdmin)
admin_site.register(Department, DepartmentAdmin)
admin_site.register(Degree_Program, DegreeProgramAdmin)
admin_site.register(Scholarship)
admin_site.register(Subject, SubjectAdmin)
admin_site.register(Purchased_Item)


