"""
Author: Christian Sta.Ana
Date: Fri Jul 18 2014
Description: Context Processors for ERDT Admin Template
"""

from django.shortcuts import *
from profiling.models import (Profile, Person)
import sys
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
            'authentication': 'auth'
        },
 
        'profiles': {
            'student': 'Student',
            'faculty_adviser': 'Faculty Adviser',
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

    userProfiles = None
    activeProfile = None

    try:
        currentUserPerson = Person.objects.get(user = currentUser.id)

        # Get all profiles of user
        userProfiles = currentUserPerson.profile_set.all()

        # Get the active profile
        if(len(userProfiles) > 1):            
            for profile in userProfiles:
                if(profile.active == True):
                    activeProfile = profile    
        elif(len(userProfiles) == 1):
            activeProfile = userProfiles[0]

    except:
        e = sys.exc_info()[0]
        print("**********Error: %s" % e)

    multi_profile = {
        'profiles' : userProfiles,
        'active_profile' : activeProfile,

    }

    return {
        'multi_profile' : multi_profile

    }



