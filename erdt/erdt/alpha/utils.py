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


def get_permissions():

    try:

        permissions = {
            'user': {
                'view': Permission.objects.get(codename='view_user'),
                'edit': Permission.objects.get(codename='change_user'),
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


def generate_permissions(user_id, role):

    try:
        current_user = User.objects.get(pk=user_id)

        # Get permissions first
        permissions = get_permissions()

        if(role == Profile.STUDENT): # Give permissions of a STUDENT

            current_user.is_superuser = False

            current_user.user_permissions.clear()

            current_user.user_permissions.add(permissions['profiling_person']['view'])
            current_user.user_permissions.add(permissions['profiling_person']['change'])
            current_user.user_permissions.add(permissions['profiling_scholarship']['view'])
            current_user.user_permissions.add(permissions['profiling_enrolled_subject']['view'])
        
        if(role == Profile.ADVISER): # Give permissions of a FACULTY ADVISER
            current_user.is_superuser = True # Temporarily give superuser permissions

        current_user.save()

    except Exception as e:
        print("Error generating permissions: %s" % e.message)

        return False

    return True
