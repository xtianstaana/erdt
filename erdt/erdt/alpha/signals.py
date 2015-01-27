"""
Author: Christian Sta.Ana
Date: Sun Sep 28 2014
Description: Contains Signals receiver functions
"""

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

# Utility methods
from utils import *

# Import Profiling Module Models 
from profiling.models import *

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

"""
Author: Christian Sta.Ana
Date: Sun Sep 28 2014
Description: Triggers before a Profile record/row have been saved
Params: default
Returns: default
Revisions:
"""
@receiver(pre_save, sender=Profile)
def profile_presave_handler(sender, **kwargs):
    try:
        saved_profile = kwargs['instance']
        target_person = saved_profile.person
        
        if saved_profile.id != None:
            if saved_profile.active:
                target_person.profile_set.exclude(id=saved_profile.id).update(active=False)
        else:
            if not target_person.profile_set.filter(active=True).exists():
                saved_profile.active = True
    except Exception as e:
        print e

@receiver(post_save, sender=Profile)
def profile_postsave_handler(sender, **kwargs):
    try:
        saved_profile = kwargs['instance']
        target_person = saved_profile.person
        active_profile = target_person.profile_set.get(active=True)
        
        if target_person.user:
            generate_permissions(target_person.user.pk, saved_profile.role)
    except Exception as e:
        print e

@receiver(post_delete, sender=Profile)
def profile_postdelete_handler(sender, **kwargs):
    try:
        deleted_profile = kwargs['instance']
        target_person = deleted_profile.person
        
        if target_person.user:
            if target_person.profile_set.count() == 0:
                target_person.user.user_permissions.clear()
            else:                
                if not target_person.profile_set.filter(active=True).exists():
                    first_profile = target_person.profile_set.first()
                    first_profile.active = True
                    first_profile.save()
    except Exception as e:
        print e