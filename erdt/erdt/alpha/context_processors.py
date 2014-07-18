"""
Author: Christian Sta.Ana
Date: Fri Jul 18 2014
Description: Context Processors for ERDT Admin Template
"""

from django.shortcuts import *

def external_urls(request):

    external_urls = {
        'dost_site':"http://www.dost.gov.ph/",
    }

    return {
        'external_urls' : external_urls
    }