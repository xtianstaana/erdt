"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains all utility functions (ex: queries, creation, deletion, etc.)
"""

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.shortcuts import render
from profiling.models import (Profile, Person)
from django.contrib.auth.decorators import login_required
from utils import *

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

import sys

@login_required
def set_active_profile(request, profile_id):

    currentUser = request.user

    try:
        selected_profile = get_object_or_404(Profile, pk = profile_id)

        # Set all profiles as inactive
        currentUserPerson = Person.objects.get(user=currentUser.id)
        for profile in currentUserPerson.profile_set.all():
            profile.active = False
            profile.save()

        # Set selected as active
        selected_profile.active = True
        selected_profile.save()

        # Generate permissions for the user's current role
        generate_permissions(currentUser.id, selected_profile.role)
    except Exception as e:
        print("Error Setting active profile: %s" % e.message)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
