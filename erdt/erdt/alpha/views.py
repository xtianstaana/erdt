"""
Author: Christian Sta.Ana
Date: Wed Jul 23 2014
Description: Contains all utility functions (ex: queries, creation, deletion, etc.)
"""
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from profiling.models import Profile, Person
from django.contrib.auth.decorators import login_required
from utils import *
import csv
from profiling.models import Profile, Person, Grant

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


@login_required
def grant_financial_releases(request, grant_id):
    my_profile = Profile.objects.filter(person__user=request.user.id, active=True)
    grant = Grant.objects.filter(id=grant_id)
    default = HttpResponse("You do not have the right permission to perform this action. This incident has been reported.", content_type="text/plain")

    if my_profile.exists() and grant.exists():
        my_profile = my_profile[0]
        grant = grant[0]

        if ((my_profile.role == Profile.UNIV_ADMIN) and (my_profile.university == grant.record_manager)) or (my_profile.role == Profile.CENTRAL_OFFICE):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename="%s.csv"' % ('ERDT GRANT FINANCIAL REPORT - ' + str(grant.awardee) + ' - ' + str(grant))

            writer = csv.writer(response)
            writer.writerow([str(grant.awardee), str(grant)])
            writer.writerow([])
            writer.writerow(['SUMMARY'])
            writer.writerow(['Line item', 'Approved budget', 'Released', 'Expenditure', 'Unexpended', 'Unreleased'])

            for line_item in grant.grant_allocation_set.all():
                try:
                    writer.writerow([
                        line_item.get_name_display(),
                        line_item.amount,
                        line_item.total_released(),
                        line_item.total_expenditure(),
                        line_item.total_unexpended(),
                        line_item.total_unreleased()
                    ])
                except:
                    pass

            writer.writerow([])
            writer.writerow(['FUND RELEASES'])
            writer.writerow(['Date released', 'Particular', 'Released', 'Liquidated', 'Unexpended'])

            for fund_release in grant.grant_allocation_release_set.all():
                try:
                    writer.writerow([
                        str(fund_release.date_released),
                        fund_release.particular(),
                        fund_release.amount_released,
                        fund_release.amount_liquidated,
                        fund_release.amount_unexpended()
                    ])
                except:
                    pass

            return response
    return default


@login_required
def create_list_equipment(request, faculty_id):
    my_profile = Profile.objects.filter(person__user=request.user.id, active=True)
    
    f_profile = Profile.objects.filter(person__pk=faculty_id, role=Profile.ADVISER)
    default = HttpResponse("You do not have the right permission to perform this action. This incident has been reported.", content_type="text/plain")

    if my_profile.exists() and f_profile.exists():
        my_profile = my_profile[0]
        f_profile = f_profile[0]

        if ((my_profile.role == Profile.UNIV_ADMIN) and (my_profile.university == f_profile.university)) or my_profile.role == Profile.CENTRAL_OFFICE:
            faculty = Person.objects.get(pk=faculty_id)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename="%s.csv"' % ('ERDT ACCOUNTABLE EQUIPMENT - ' + faculty.name())

            writer = csv.writer(response)
            writer.writerow(['ERDT Faculty Adviser:', faculty.__str__()])
            writer.writerow([])
            writer.writerow(['Date Released', 'Property no.', 'Description', 'Status', 'Payee'])

            for e in faculty.equipments.all():
                try:
                    writer.writerow([
                        str(e.date_released), 
                        e.property_no, 
                        e.description, 
                        e.get_status_display(),
                        str(e.payee)])
                except:
                    pass

            return response
    return default

@login_required
def create_list_advisees(request, faculty_id):
    my_profile = Profile.objects.filter(person__user=request.user.id, active=True)
    
    f_profile = Profile.objects.filter(person__pk=faculty_id, role=Profile.ADVISER)
    default = HttpResponse("You do not have the right permission to perform this action. This incident has been reported.", content_type="text/plain")

    if my_profile.exists() and f_profile.exists():
        my_profile = my_profile[0]
        f_profile = f_profile[0]

        if ((my_profile.role == Profile.UNIV_ADMIN) and (my_profile.university == f_profile.university)) or my_profile.role == Profile.CENTRAL_OFFICE:
            faculty = Person.objects.get(pk=faculty_id)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename="%s.csv"' % ('ERDT ADVISEES - ' + faculty.name())

            writer = csv.writer(response)
            writer.writerow(['ERDT Faculty Adviser:', faculty.__str__()])
            writer.writerow([])
            writer.writerow(['Scholar', 'Email Address', 'Scholarship Status', 'Degree Program', 'Lateral?', 'Start Date', 'End Date', 'Date of Graduation'])

            for sch in faculty.advisees.order_by('scholarship_status', 'awardee'):
                try:
                    writer.writerow([
                        sch.awardee.__str__(), 
                        sch.awardee.email_address, 
                        sch.get_scholarship_status_display(), 
                        sch.degree_program.__str__(),
                        sch.lateral,
                        sch.start_date.isoformat(),
                        sch.end_date.isoformat(),
                        sch.end_grad_program.isoformat()])
                except:
                    pass

            return response
    return default
