"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains all utility functions (ex: queries, creation, deletion, etc.)
"""
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from profiling.models import Profile, Person
from django.contrib.auth.decorators import login_required
from utils import *

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

@login_required
def set_active_profile(request, profile_id):

    currentUser = request.user

    try:
        selected_profile = get_object_or_404(Profile, pk=profile_id)

        currentUserPerson = Person.objects.get(user=currentUser.id)
        selected_profile.active = True
        selected_profile.save()

    except Exception as e:
        print("Error Setting active profile: %s" % e.message)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
