"""
Author: Christian Sta.Ana
Date: Sun Sep 28 2014
Description: Contains Signals receiver functions
"""

import sys

from django.db.models.signals import pre_save, post_save
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
Description: Triggers after a Person record/row have been saved
Params: default
Returns: default
Revisions:
"""
@receiver(post_save, sender=Person)
def person_postsave_handler(sender, **kwargs):
    try:
        saved_person = kwargs['instance']

        # Check if person being saved has an existing student profile
        user_profiles = saved_person.profile_set.all()

        has_existing_student_profile = False
        existing_student_profile = None

        if(len(user_profiles) > 0):            
            for user_profile in user_profiles:
                if user_profile.role == Profile.STUDENT:
                    has_existing_student_profile = True
                    existing_student_profile = user_profile

        if not has_existing_student_profile:
            # Create student profile for user
            student_profile = Profile(role = Profile.STUDENT, person = saved_person)

            # Set all profiles as inactive
            for user_profile in user_profiles:
                user_profile.active = False
                user_profile.save()

            # Set selected as active
            student_profile.active = True

            # Search for scholarship
            user_scholarship = Scholarship.objects.get(scholar = saved_person.pk) 

            if(user_scholarship):
                student_profile.university = user_scholarship.high_degree_univ

            student_profile.save()
        else:
            # Save existing student profile with current university
            user_scholarship = Scholarship.objects.get(scholar = saved_person.pk) 

            if(user_scholarship):
                existing_student_profile.university = user_scholarship.high_degree_univ

            existing_student_profile.save()
    except Exception as e:
        print e

"""
Author: Christian Sta.Ana
Date: Sun Sep 28 2014
Description: Triggers after a Scholarship record/row have been saved
Params: default
Returns: default
Revisions:
"""
@receiver(post_save, sender=Scholarship)
def scholarship_postsave_sch(sender, **kwargs):
    try:
        saved_scholarship = kwargs['instance']

        # Check if adviser has adviser profile
        target_person = saved_scholarship.adviser

        user_profiles = target_person.profile_set.all()

        has_existing_adviser_profile = False
        existing_adviser_profile = None

        if(len(user_profiles) > 0):            
            for user_profile in user_profiles:
                if(user_profile.role == Profile.ADVISER):
                    has_existing_adviser_profile = True
                    existing_adviser_profile = user_profile


        if(has_existing_adviser_profile is False):
            # Create adviser profile for user
            adviser_profile = Profile(role = Profile.ADVISER, person = target_person, 
                university = saved_scholarship.high_degree_univ)

            # Set all profiles as inactive
            for user_profile in user_profiles:
                user_profile.active = False
                user_profile.save()

            # Set selected as active
            adviser_profile.active = True  
            adviser_profile.save()  
        else:
            # Save current adviser profile with university
            if(saved_scholarship.high_degree_univ):
                existing_adviser_profile.university = saved_scholarship.high_degree_univ
                existing_adviser_profile.save()

        # Change university of student profile if university is different
        target_scholar = saved_scholarship.scholar

        scholar_profiles = target_scholar.profile_set.all()

        has_existing_student_profile = False

        student_university = None
        student_profile = None

        if(len(scholar_profiles) > 0):            
            for user_profile in scholar_profiles:
                if(user_profile.role == Profile.STUDENT):
                    has_existing_student_profile = True
                    student_university = user_profile.university
                    student_profile = user_profile

        if(has_existing_student_profile and student_university != saved_scholarship.high_degree_univ):
            student_profile.university = saved_scholarship.high_degree_univ
            student_profile.save()

    except Exception as e:
        #print e
        pass


"""
Author: Christian Sta.Ana
Date: Sun Sep 28 2014
Description: Triggers after a Profile record/row have been saved
Params: default
Returns: default
Revisions:
"""
@receiver(pre_save, sender=Profile)
def profile_presave_handler(sender, **kwargs):
    try:
        saved_profile = kwargs['instance']

        target_person = saved_profile.person

        print 'presave profile'

        if(saved_profile.pk is None):
            print 'newly created profile, set as active'
            # Set all profiles as inactive
            for user_profile in target_person.profile_set.all():
                user_profile.active = False
                user_profile.save()

            saved_profile.active = True

            generate_permissions(target_person.user.pk, saved_profile.role)


    except Exception as e:
        #print e
        pass


