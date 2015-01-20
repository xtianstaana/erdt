from django.db.models import get_app, get_models

# Import Profiling Module Models 
from profiling.models import Profile, Person
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
import json

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
        reporting_app = get_app(constants['constants']['apps']['reporting'])
        profiling_app = get_app(constants['constants']['apps']['profiling'])

        models = get_models(reporting_app) + get_models(profiling_app)
   

        # Create permissions for user
        user_content_type = ContentType.objects.get_for_model(User)
        try:
            user_permission = Permission.objects.create(
                codename=('view_user'),
                name=('Can view user'),
                content_type=user_content_type)
        except:
            pass

        #print 'Creating readonly permissions'

        for model in models:
            # Create permissions for profiling models
            content_type = ContentType.objects.get_for_model(model)

            #print ('%s' % model._meta.model_name)

            try:
                permission = Permission.objects.create(
                    codename=('view_%s' % model._meta.model_name ),
                    name=('Can view %s' % model._meta.verbose_name),
                    content_type=content_type)
            except:
                pass

    except Exception as e:
        #print("Error Creating ReadOnly Perm: %s" % e.message)
        return False

    return True


def f(user, permission, model_names, all_models):
    
    ex = [e for e in all_models if e not in model_names]

    for model_name in ex:
        p = Permission.objects.get(codename='_'.join((permission, model_name)))
        if p.user_set.filter(id=user.id).exists():
            print user.username, 'removing', p.codename
            p.user_set.remove(user)

    for model_name in model_names:
        p = Permission.objects.get(codename='_'.join((permission, model_name)))
        if not p.user_set.filter(id=user.id).exists():
            print user.username, 'adding', p.codename
            p.user_set.add(user)

"""
Author: Christian Sta.Ana
Date: Aug 2014
Description: Generates permissions for the active profile/role
Params: default
Returns: default
Revisions:
"""
def generate_permissions(user_id, role):

    print 'generating permissions for', user_id, role

    try:
        current_user = User.objects.get(pk=user_id)

        with open('erdt/alpha/permission_set.json') as permission_file:
            permission_set = json.load(permission_file)

        all_models = permission_set.keys()

        for p in ('add', 'change', 'delete'):
            p_list = [ mod_name for mod_name in permission_set if role in permission_set[mod_name][p] ]
            f(current_user, p, p_list, all_models)            

        if role == Profile.CENTRAL_OFFICE:
            if not current_user.is_superuser:
                current_user.is_superuser = True
                current_user.save()
        else:
            if current_user.is_superuser:
                current_user.is_superuser = False
                current_user.save()

        return True
    except Exception as e:
        print("Error generating permissions: %s" % e)
    
    return False

def force_update_permissions():
    user_roles = [(p.user.pk, p.profile_set.get(active=True).role) for p in Person.objects.filter(user__isnull=False)]

    for user_role in user_roles:
        generate_permissions(*user_role)