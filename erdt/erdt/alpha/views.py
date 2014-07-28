"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains all utility functions (ex: queries, creation, deletion, etc.)
"""

from django.shortcuts import render


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

