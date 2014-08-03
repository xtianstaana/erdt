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


def turn_form_friendly(dict, exclude_list, label_dict):

    form_friendly_dict = []
        
    for label, value in dict.iteritems():
        
        if(label not in exclude_list):

            form_friendly_field = {}

            # clean label
            clean_label = label
            if(label in label_dict):
                clean_label = label_dict['label']
            else:
                clean_label = label.replace('_', ' ')
                clean_label = clean_label.capitalize()

            form_friendly_field['name'] = label
            form_friendly_field['label'] = clean_label
            form_friendly_field['value'] = value

            form_friendly_dict.append(form_friendly_field)

    return form_friendly_dict

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
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
