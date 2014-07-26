"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains Admin Customization functions
"""


from django.contrib.admin import AdminSite
from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin import ModelAdmin, actions
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
    """
    @never_cache
    def index(self, request, extra_context=None):
        erdtIndexTempRes = super(ERDTAdminSite, self).index(request)

        erdtIndexTempRes.context_data['title'] = constants['constants']['site']['index_title']
        # get current user data
        currentUser = request.user
        erdtIndexTempRes.context_data['current_user'] = currentUser

        return erdtIndexTempRes

class ProfileSite(ModelAdmin):
    list_display = ('person', 'role') 
    list_filter = ('role',)

class DegreeProgramSite(ModelAdmin):
    list_display = ('program', 'degree', 'department')
    list_filter = ('degree', 'department__university__name')

class DepartmentSite(ModelAdmin):
    list_display = ('name', 'university',)
    list_filter = ('university',)

class PersonSite(ModelAdmin):
    list_display = ('__unicode__', 'email_address', 'mobile_number')
    search_fields = ('first_name', 'middle_name', 'last_name')

class SubjectSite(ModelAdmin):
    list_display = ('course_title', 'course_units', 'university')
    list_filter = ('university',)

class UniversitySite(ModelAdmin):
    list_display = ('name', 'no_semester', 'with_summer', 'email_address', 'landline_number')

# Set the admin_site object as the custom ERDT Admin Site
admin_site = ERDTAdminSite()

# Register Django models
admin_site.register(User)

# Register Profiling models
admin_site.register(Profile, ProfileSite)
admin_site.register(Person, PersonSite) 
admin_site.register(University, UniversitySite)
admin_site.register(Department, DepartmentSite)
admin_site.register(Degree_Program, DegreeProgramSite)
admin_site.register(Scholarship)
admin_site.register(Subject, SubjectSite)
admin_site.register(Purchased_Item)


