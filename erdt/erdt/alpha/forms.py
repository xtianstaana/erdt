"""
Author: Christian Sta.Ana
Date: Sat Aug 09 2014
Description: Contains ModelForm implementation
"""

import sys

from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from django.db import models

from suit.widgets import *
from django.forms.widgets import *

# Utility methods
from views import *

# Import Profiling Module Models 
from profiling.models import (Profile, Person, University, Department,
    Degree_Program, Scholarship, Subject, Purchased_Item, Enrolled_Subject, Item_Tag)

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)


"""
Author: Christian Sta.Ana
Date: Sat Aug 09 2014
Description: ModelForm for Person object
"""
"""
class PersonForm(ModelForm):
    class Meta:
        widgets = {

        }
"""

"""
Author: Christian Sta.Ana
Date: Sat Aug 09 2014
Description: ModelForm for User object
"""

class UserForm(ModelForm):
    class Meta:
        widgets = {
            'password': PasswordInput
        }


