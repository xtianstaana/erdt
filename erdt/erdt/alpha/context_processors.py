"""
Author: Christian Sta.Ana
Date: Fri Jul 18 2014
Description: Context Processors for ERDT Admin Template
"""

from django.shortcuts import *
from profiling.models import (Profile, Person)

"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Link/URL Constants
Params: HttpRequest request
Returns: Dictionary containing external_urls dictionary
"""
def external_urls(request):

    external_urls = {
        'dost_site':'http://www.dost.gov.ph/',
    }

    return {
        'external_urls' : external_urls
    }

"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: String Constants (General Site, Profile, Search, etc./other modules)
Params: HttpRequest request
Returns: Dictionary containing constants dictionary
"""
def constants(request):

    constants = {
        
        'site': {
            'site_title': 'DOST ERDT',
            'project_title': 'ERDT Scholars Management System',
            'index_title': 'Profile',
            'index_caption': 'My Profile'
        },

        'apps': {
            'profiling': 'profiling',
            'financial': 'financial',
            'authentication': 'auth'

        },
 
        'profiles': {
            'student': 'Student',
            'faculty_adviser': 'Faculty',
            'consortium_admin': 'Consortium Administrator',
            'erdt_central_office': 'ERDT Central Office',
            'dost_office': 'DOST Office'
        }
    }

    return {
        'constants': constants
    }

"""
Author: Christian Sta.Ana
Date: Sat Aug 2 2014
Description: For users with mutiple profiles
Params: HttpRequest request
Returns: Dictionary containing all profiles and the active profile
"""
def multi_profile(request):

    currentUser = request.user

    try:
        currentUserPerson = Person.objects.get(user = currentUser.id)
        userProfiles = currentUserPerson.profile_set.all()
        activeProfile = userProfiles.get(active=True)
        activeRole = activeProfile.role
        is_admin = activeRole in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN, Profile.DOST)

    except Exception as e:
        userProfiles = None
        activeProfile = None
        activeRole = None
        is_admin = None
        print("**********Error at context_processor: %s" % e)

    multi_profile = {
        'profiles' : userProfiles,
        'active_profile' : activeProfile,
        'active_role' : activeRole,
        'is_admin' : is_admin,
    }

    return {
        'multi_profile' : multi_profile,
    }



