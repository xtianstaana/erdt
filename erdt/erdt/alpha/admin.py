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

# Set the admin_site object as the custom ERDT Admin Site
admin_site = ERDTAdminSite()

# Register Django models
admin_site.register(User)

# Register Profiling models
admin_site.register(Profile)
admin_site.register(Person)
admin_site.register(University)
admin_site.register(Department)
admin_site.register(Degree_Program)
admin_site.register(Scholarship)
admin_site.register(Subject)
admin_site.register(Purchased_Item)


