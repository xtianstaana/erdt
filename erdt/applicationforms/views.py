from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from applicationforms import forms
from applicationforms.models import *
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from profiling.models import *
import base64
import sys
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
import uuid
import datetime
import time

#######################################################################################
# Pre-registration
#######################################################################################
def confirm_registration_dummy(request):
    return render(request, 'applicationforms/preregistration.html', {})

def display_prereg_form(request):
    form = forms.PreRegistrationForm()
    return render(request, 'applicationforms/preregistration.html', {'form':form})

def submit_prereg_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            raise Http404("Password mismatch")

        try:
            # Create user
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.is_active = False
            user.save()

            # Create person
            person = Person(first_name = firstname, last_name = lastname, user = user)
            person.save()

            print "Person id: %d" % person.id

            # Create profile
            profile = Profile(role = 'REGISTRANT', person = person, active = True)
            profile.save()

            # Send email
            body = ("Dear %s %s \n" % (firstname, lastname))
            
            # generate token
            generated_token = str(uuid.uuid1()) + "-" + base64.b64encode(username)
            print generated_token

            #confirm_link = reverse('confirm-preregistration-dummy')
            #confirm_link += generated_token
            confirm_link = reverse('confirm-preregistration', kwargs={'confirmation_token':'TOKEN'})
            confirm_link = confirm_link.replace('TOKEN', generated_token)

            body += "Confirmation link: %s" % (request.build_absolute_uri(confirm_link))

            print body
            print "User id: %d" % user.id
            print "Person id: %d" % person.id
            
            #result = send_mail('[DOST ERDT] Confirm your registration', body, settings.EMAIL_HOST_USER, [email])
            msg = EmailMessage('[DOST ERDT] Confirm your registration', body, settings.EMAIL_HOST_USER, [email])
            result = msg.send()

            print ("Result: %s" % result)

        except Exception as e:
            print("Error Registering User: %s" % e)
            raise Http404("Error on submission: %s" % e.message)

        return render(request, 'applicationforms/preregistration_submit.html', {'email':email})

    else:
        raise Http404("Error on submission")

def confirm_registration(request, confirmation_token):
    if confirmation_token is not None:
        splitted = (confirmation_token).split("-")
        
        username = base64.b64decode(splitted[len(splitted)-1])

        print "Username: %s" % username

        user = User.objects.get(username = username)

        print "User Id: %d" % user.id
        print "Active: %r" % user.is_active

        user.is_staff = True
        user.is_active = True

        print "Activated"
        user.save()

    else :
        raise Http404("Error: %s" % e.message)
    # To be done: complete this method
    return render(request, 'applicationforms/preregistration_finished.html', {})

@login_required
def index(request):
    # Get current active application period
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get ERDTForm for this application period
    try:
        erdt_form = ERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        erdt_form = None

    # Get UP Grad Form for this application period
    try:
        upgrad_form = UPGradForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
        print "UP Grad Form retrieved: %d" % upgrad_form.id 
    except Exception as e:
        upgrad_form = None

    # Get UPD ERDTForm for this application period
    try:
        upderdt_form = UPDERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
        print "UPD ERDT Form retrieved: %d" % upderdt_form.id 
    except Exception as e:
        upderdt_form = None

    # Get Recommendation forms for this application period
    try:
        recommendation_forms = RecommendationForm.objects.filter(application_period_id = application_period.pk, sent_by_id = current_user.id)
    
        if len(recommendation_forms) == 0:
            recommendation_forms = None

    except Exception as e:
        recommendation_forms = None
    

    return render(request, 'applicationforms/index.html', {'erdt_form' : erdt_form, 
                                                            'upgrad_form' : upgrad_form, 
                                                            'upderdt_form' : upderdt_form, 
                                                            'recommendation_forms' : recommendation_forms})


#######################################################################################
# ERDT Application Form
#######################################################################################
@login_required
def edit_erdt_form(request):
    # Get current active application period
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get ERDTForm for this application period
    try:
        erdt_form = ERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
        print "ERDT Form retrieved: %d" % erdt_form.id 
    except Exception as e:
        erdt_form = None

    if erdt_form is None:
        print "No erdt form yet. Creating"
        erdt_form = ERDTForm(application_period_id = application_period.pk, created_by_id = current_user.id, created_date = datetime.datetime.now(), last_modified_date = datetime.datetime.now(), status = 'In Progress')
        erdt_form.save()

    form = forms.ERDTFormApplicationForm(instance = erdt_form)

    if erdt_form.status != 'Submitted':
        return render(request, 'applicationforms/erdt_form.html', {'form' : form})
    else:
        return index(request)

@login_required
def confirm_erdt_form(request):
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get ERDTForm for this application period
    try:
        erdt_form = ERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        erdt_form = None
   
    erdt_form.last_modified_date = datetime.datetime.now() 
    edited_erdt_form = forms.ERDTFormApplicationForm(request.POST, instance = erdt_form)
    
    if edited_erdt_form.is_valid():
        saved_erdt_form = edited_erdt_form.save()
    else:

        return edit_erdt_form(request)

    return index(request)


#######################################################################################
# UP Graduate Application Form
#######################################################################################
@login_required
def edit_upgrad_form(request):
    # Get current active application period
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get ERDTForm for this application period
    try:
        upgrad_form = UPGradForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        upgrad_form = None

    if upgrad_form is None:
        print "No erdt form yet. Creating"
        upgrad_form = UPGradForm(application_period_id = application_period.pk, created_by_id = current_user.id, created_date = datetime.datetime.now(), last_modified_date = datetime.datetime.now(), status = 'In Progress')
        upgrad_form.save()

    form = forms.UPGradFormApplicationForm(instance = upgrad_form)

    if upgrad_form.status != 'Submitted':
        return render(request, 'applicationforms/upgrad_form.html', {'form' : form})
    else:
        return index(request)

@login_required
def confirm_upgrad_form(request):
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get UPGradForm for this application period
    try:
        upgrad_form = UPGradForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        upgrad_form = None
   
    upgrad_form.last_modified_date = datetime.datetime.now() 
    edited_upgrad_form = forms.UPGradFormApplicationForm(request.POST, instance = upgrad_form)
    
    if edited_upgrad_form.is_valid():
        saved_upgrad_form = edited_upgrad_form.save()
    else:

        return edit_upgrad_form(request)

    return index(request)


#######################################################################################
# UPD - ERDT Application Form
#######################################################################################
@login_required
def edit_upderdt_form(request):
    # Get current active application period
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get ERDTForm for this application period
    try:
        upderdt_form = UPDERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        upderdt_form = None

    if upderdt_form is None:
        print "No erdt form yet. Creating"
        upderdt_form = UPDERDTForm(application_period_id = application_period.pk, created_by_id = current_user.id, created_date = datetime.datetime.now(), last_modified_date = datetime.datetime.now(), status = 'In Progress')
        upderdt_form.save()

    form = forms.UPDERDTFormApplicationForm(instance = upderdt_form)

    if upderdt_form.status != 'Submitted':
        return render(request, 'applicationforms/upderdt_form.html', {'form' : form})
    else:
        return index(request)

@login_required
def confirm_upderdt_form(request):
    current_date = datetime.date.today()
    current_user = request.user
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get UPDERDTForm for this application period
    try:
        upderdt_form = UPDERDTForm.objects.get(application_period_id = application_period.pk, created_by_id = current_user.id)
    except Exception as e:
        upderdt_form = None

    upderdt_form.last_modified_date = datetime.datetime.now() 
    edited_upderdt_form = forms.UPDERDTFormApplicationForm(request.POST, instance = upderdt_form)
    
    if edited_upderdt_form.is_valid():
        saved_upderdt_form = edited_upderdt_form.save()
    else:

        return edit_upderdt_form(request)

    return index(request)



#######################################################################################
# Recommendation Form
#######################################################################################
@login_required
def add_recommendation_form(request):

    current_date = datetime.date.today()
    current_user = request.user
    
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    # Get Recommendation forms for this application period
    try:
        recommendation_forms = RecommendationForm.objects.filter(application_period_id = application_period.id, sent_by_id = current_user.id)
    
        if len(recommendation_forms) == 0:
            recommendation_forms = None

    except Exception as e:
        recommendation_forms = None

    return render(request, 'applicationforms/add_recommendation_form.html', {'recommendation_forms':recommendation_forms})

@login_required
def send_recommendation_form(request):

    current_date = datetime.date.today()
    current_user = request.user
    
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    if request.method == "POST":
        email = request.POST.get("email")
        fullname = request.POST.get("name")

        try:
            # generate token
            generated_token = uuid.uuid1()
            security_code = base64.b64encode("%lf" % time.time())[13:19]
            token = Token(created_date = current_date, code = generated_token, security_code = security_code)
            token.save()

            # create recommendation form
            recommendation = RecommendationForm()
            recommendation.token = token
            recommendation.sent_by = current_user
            recommendation.created_by = current_user
            recommendation.status = RecommendationForm.NOT_STARTED
            recommendation.professor_email = email
            recommendation.professor_name = fullname
            recommendation.created_date = datetime.datetime.now()
            recommendation.sent_date = datetime.datetime.now()
            recommendation.application_period = application_period
            recommendation.save()

            # send to email
            edit_link = reverse('edit-recommendation-form', kwargs={'token_str':generated_token})
            #edit_link += generated_token
            
            body = "Fill recommendation: %s \n" % (request.build_absolute_uri(edit_link))
            body += "Your passcode: %s \n" % security_code

            print body
            
            #result = send_mail('[DOST ERDT] Confirm your registration', body, settings.EMAIL_HOST_USER, [email])
            msg = EmailMessage('[DOST ERDT] Recommendation', body, settings.EMAIL_HOST_USER, [email])
            result = msg.send()

            print ("Result: %s" % result)


        except Exception as e:
            print("Error: %s" % e)

    return add_recommendation_form(request)

def edit_recommendation_form(request, token_str):

    current_date = datetime.date.today()
    
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    
        # Query recommendation form
        recommendation_form = RecommendationForm.objects.get(application_period_id = application_period.id, token__code = token_str)

        if request.method == 'POST':

            edited_recommendation_form = forms.RecommendationFormApplicationForm(request.POST, instance = recommendation_form)
            if edited_recommendation_form.is_valid():
                saved_recommendation_form = edited_recommendation_form.save()

        form = forms.RecommendationFormApplicationForm(instance = recommendation_form)

        if recommendation_form.status != 'Submitted':
            return render(request, 'applicationforms/recommendation_form.html', {'form' : form, 'token' : recommendation_form.token.code})
        else:
            return render(request, 'applicationforms/submitted_recommendation_form.html', {})

    except Exception as e:
            raise Http404("Error: %s" % e.message)

@login_required
def delete_recommendation_form(request):
    return index(request)


def confirm_recommendation_form(request):
    current_date = datetime.date.today()
    try:
        application_period = ApplicationPeriod.objects.get(active = True, start_date__lte = current_date, end_date__gte = current_date)
    except Exception as e:
            raise Http404("Error: %s" % e.message)

    token = request.POST.get('token')

    # Query recommendation form
    recommendation_form = RecommendationForm.objects.get(application_period_id = application_period.id, token__code = request.POST.get('token'))

    form = forms.RecommendationFormApplicationForm(instance = recommendation_form)

    edited_recommendation_form = forms.RecommendationFormApplicationForm(request.POST, instance = recommendation_form)
    
    if edited_recommendation_form.is_valid():
        saved_recommendation_form = edited_recommendation_form.save()
    else:
        return edit_recommendation_form(request)

    return edit_recommendation_form(request)

