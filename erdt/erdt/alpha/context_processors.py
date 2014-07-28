"""
Author: Christian Sta.Ana
Date: Fri Jul 18 2014
Description: Context Processors for ERDT Admin Template
"""

from django.shortcuts import *

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
        }
    }

    return {
        'constants': constants
    }