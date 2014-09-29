from django.db.models import get_app, get_models

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Item_Tag)

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

import sys

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

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

"""
Author: Christian Sta.Ana
Date: Aug 2014
Description: Creates readonly permissions for this site
Params: default
Returns: default
Revisions:
"""
def create_readonly_permissions():

    try:
        profiling_app = get_app(constants['constants']['apps']['profiling'])

        models = get_models(profiling_app)

        print models

        # Create permissions for user
        user_content_type = ContentType.objects.get_for_model(User)
        user_permission = Permission.objects.create(codename=('view_user'),
                                                    name=('Can view user'),
                                                    content_type=user_content_type)

        for model in models:
            # Create permissions for profiling models
            content_type = ContentType.objects.get_for_model(model)

            permission = Permission.objects.create(codename=('view_%s' % model._meta.verbose_name.lower().replace(' ', '_') ),
                                                    name=('Can view %s' % model._meta.verbose_name),
                                                    content_type=content_type)

    except Exception as e:
        print e
        print("Error Creating ReadOnly Perm: %s" % e.message)

        return False

    return True

"""
Author: Christian Sta.Ana
Date: Aug 2014
Description: Creates dictionary of permissions object for easy access
Params: default
Returns: default
Revisions:
"""
def get_permissions():

    try:

        permissions = {
            'user': {
                'view': Permission.objects.get(codename='view_user'),
                'change': Permission.objects.get(codename='change_user'),
                'add': Permission.objects.get(codename='add_user'),
                'delete': Permission.objects.get(codename='delete_user')
            }
        }

        profiling_app = get_app(constants['constants']['apps']['profiling'])

        models = get_models(profiling_app)

        for model in models:
            if not model._meta.db_table in permissions:
                permissions[model._meta.db_table] = {}
                permissions[model._meta.db_table]['view'] = Permission.objects.get(codename = ('view_%s' % model._meta.verbose_name.lower().replace(' ', '_') ))
                permissions[model._meta.db_table]['change'] = Permission.objects.get(codename = ('change_%s' % model._meta.verbose_name.lower().replace(' ', '_') ))
                permissions[model._meta.db_table]['add'] = Permission.objects.get(codename = ('add_%s' % model._meta.verbose_name.lower().replace(' ', '_') ))
                permissions[model._meta.db_table]['delete'] = Permission.objects.get(codename = ('delete_%s' % model._meta.verbose_name.lower().replace(' ', '_') ))

        return permissions

    except Exception as e:
        print("Error Getting Permissions: %s" % e.message)

        return None

"""
Author: Christian Sta.Ana
Date: Aug 2014
Description: Generates permissions for the active profile/role
Params: default
Returns: default
Revisions:
"""
def generate_permissions(user_id, role):

    print 'generating permissions'

    try:
        current_user = User.objects.get(pk=user_id)

        # Get permissions first
        permissions = get_permissions()

        current_user.is_staff = True

        if(role == Profile.STUDENT): # Give permissions of a STUDENT

            current_user.is_superuser = False

            current_user.user_permissions.clear()

            current_user.user_permissions.add(permissions['profiling_person']['view'])
            current_user.user_permissions.add(permissions['profiling_person']['change'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['view'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['view'])

        if(role == Profile.STUDENT): # Give permissions of a ADVISER
            # Same as STUDENT permissions temporarily
            current_user.is_superuser = False

            current_user.user_permissions.clear()

            current_user.user_permissions.add(permissions['profiling_person']['view'])
            current_user.user_permissions.add(permissions['profiling_person']['change'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['view'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['view'])

        if(role == Profile.UNIV_ADMIN): # Give permissions of a UNIV_ADMIN

            current_user.is_superuser = False

            current_user.user_permissions.clear()

            current_user.user_permissions.add(permissions['profiling_university']['view'])
            current_user.user_permissions.add(permissions['profiling_department']['view'])
            current_user.user_permissions.add(permissions['profiling_degree_program']['view'])
            current_user.user_permissions.add(permissions['user']['view'])
            current_user.user_permissions.add(permissions['profiling_person']['view'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['view'])
            current_user.user_permissions.add(permissions['profiling_profile']['view'])
            current_user.user_permissions.add(permissions['profiling_item_tag']['view'])
            current_user.user_permissions.add(permissions['profiling_purchased_item']['view'])
            current_user.user_permissions.add(permissions['profiling_subject']['view'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['view'])

            current_user.user_permissions.add(permissions['profiling_university']['add'])
            current_user.user_permissions.add(permissions['profiling_department']['add'])
            current_user.user_permissions.add(permissions['profiling_degree_program']['add'])
            current_user.user_permissions.add(permissions['user']['add'])
            current_user.user_permissions.add(permissions['profiling_person']['add'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['add'])
            current_user.user_permissions.add(permissions['profiling_profile']['add'])
            current_user.user_permissions.add(permissions['profiling_item_tag']['add'])
            current_user.user_permissions.add(permissions['profiling_purchased_item']['add'])
            current_user.user_permissions.add(permissions['profiling_subject']['add'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['add'])

            current_user.user_permissions.add(permissions['profiling_university']['change'])
            current_user.user_permissions.add(permissions['profiling_department']['change'])
            current_user.user_permissions.add(permissions['profiling_degree_program']['change'])
            current_user.user_permissions.add(permissions['user']['change'])
            current_user.user_permissions.add(permissions['profiling_person']['change'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['change'])
            current_user.user_permissions.add(permissions['profiling_profile']['change'])
            current_user.user_permissions.add(permissions['profiling_item_tag']['change'])
            current_user.user_permissions.add(permissions['profiling_purchased_item']['change'])
            current_user.user_permissions.add(permissions['profiling_subject']['change'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['change'])

            current_user.user_permissions.add(permissions['profiling_university']['delete'])
            current_user.user_permissions.add(permissions['profiling_department']['delete'])
            current_user.user_permissions.add(permissions['profiling_degree_program']['delete'])
            current_user.user_permissions.add(permissions['user']['delete'])
            current_user.user_permissions.add(permissions['profiling_person']['delete'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['delete'])
            current_user.user_permissions.add(permissions['profiling_profile']['delete'])
            current_user.user_permissions.add(permissions['profiling_item_tag']['delete'])
            current_user.user_permissions.add(permissions['profiling_purchased_item']['delete'])
            current_user.user_permissions.add(permissions['profiling_subject']['delete'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['delete'])
        
        if(role == Profile.CENTRAL_OFFICE): # Give permissions of a CENTRAL OFFICE
            current_user.is_superuser = True 

        if(role == Profile.DOST): # Give permissions of a DOST
            current_user.is_superuser = False

            current_user.user_permissions.clear()

            current_user.user_permissions.add(permissions['profiling_university']['view'])
            current_user.user_permissions.add(permissions['profiling_department']['view'])
            current_user.user_permissions.add(permissions['profiling_degree_program']['view'])
            current_user.user_permissions.add(permissions['user']['view'])
            current_user.user_permissions.add(permissions['profiling_person']['view'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['view'])
            current_user.user_permissions.add(permissions['profiling_profile']['view'])
            current_user.user_permissions.add(permissions['profiling_item_tag']['view'])
            current_user.user_permissions.add(permissions['profiling_purchased_item']['view'])
            current_user.user_permissions.add(permissions['profiling_subject']['view'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['view'])

        current_user.save()

    except Exception as e:
        print("Error generating permissions: %s" % e.message)

        return False

    return True
