"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains Admin Customization functions
"""

import sys

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.forms.models import model_to_dict
from forms import *

# Utility methods
from utils import *

# Import Profiling Module Models 
from profiling.models import *

from reporting.models import *

# Import Constants
from context_processors import constants, external_urls
constants = constants(None)
external_urls = external_urls(None)

# Import Custom ModelAdmin
from custommodeladmin.user import UserAdmin
from custommodeladmin.person import PersonAdmin
from custommodeladmin.university import UniversityAdmin
from custommodeladmin.degree_program import DegreeProgramAdmin

from custommodeladmin.fund_release import GrantAllocationReleaseAdmin
from custommodeladmin.equipment import PurchasedItemAdmin
from custommodeladmin.research_dissemination import ResearchDisseminationAdmin

from custommodeladmin.grants import *
from custommodeladmin.scholarship import ScholarshipAdmin
#from custommodeladmin.visiting_professor import VisitingProfessorAdmin

from custommodeladmin.university_report import UniversityReportAdmin
from custommodeladmin.individual_report import IndividualReportAdmin

"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Overrides the default Django AdminSite object
"""
class ERDTAdminSite(AdminSite):

    """
    Author: Christian Sta.Ana
    Date: Wed Jul 23 2014
    Description: Overrides the index view of the AdminSite
    Params: default
    Returns: default
    Revisions:
    07/26/14 - Retrieval of profile and person data added
    """
    @never_cache
    def index(self, request, extra_context=None):
        erdtIndexTempRes = super(ERDTAdminSite, self).index(request)

        erdtIndexTempRes.context_data['title'] = constants['constants']['site']['index_title']
        
        # get current user data
        currentUser = request.user

        currentUserPerson = None
        userFields = None
        personFields = None

        try:
            currentUserPerson = Person.objects.get(user=currentUser.id)
        except:
            e = sys.exc_info()[0]
            #print("Error: %s" % e)

        # Excluded fields list
        user_exclude = ['first_name', 'last_name', 'is_active', 'email', 'is_superuser', 'is_staff', 'groups', 
            'password', 'id', 'date_joined', 'user_permissions']
        person_exclude = ['photo', 'id', 'user']

        if(currentUser):
            userFields = turn_form_friendly(model_to_dict(currentUser), user_exclude, {})

        if(currentUserPerson):
            currentUserPerson.sex = currentUserPerson.get_sex_display()
            currentUserPerson.civil_status = currentUserPerson.get_civil_status_display()
            personFields = turn_form_friendly(model_to_dict(currentUserPerson), person_exclude, {})

        erdtIndexTempRes.context_data['current_user'] = currentUser
        erdtIndexTempRes.context_data['current_user_person'] = currentUserPerson

        erdtIndexTempRes.context_data['user_fields'] = userFields
        erdtIndexTempRes.context_data['person_fields'] = personFields

        return erdtIndexTempRes


# Set the admin_site object as the custom ERDT Admin Site
admin_site = ERDTAdminSite()

# Register Django models
admin_site.register(User, UserAdmin)

# Programatically create permissions
print 'Create Readonly'
create_readonly_permissions()

admin_site.register(Sandwich_Program, SandwichAdmin)
admin_site.register(Person, PersonAdmin) 
admin_site.register(University, UniversityAdmin)
admin_site.register(Degree_Program, DegreeProgramAdmin)
admin_site.register(Scholarship, ScholarshipAdmin)
admin_site.register(Grant_Allocation_Release, GrantAllocationReleaseAdmin) 
admin_site.register(Equipment, PurchasedItemAdmin)
admin_site.register(Research_Dissemination, ResearchDisseminationAdmin)
admin_site.register(Visiting_Professor_Grant, VisitingProfessorAdmin)
admin_site.register(ERDT_Scholarship_Special, Scholarship2Admin)
admin_site.register(Postdoctoral_Fellowship, PostdoctoralAdmin)
admin_site.register(FRDG, FRDGAdmin)
admin_site.register(FRGT, FRGTAdmin)
admin_site.register(Individual_Report, IndividualReportAdmin)
admin_site.register(University_Report, UniversityReportAdmin)