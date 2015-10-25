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
import datetime

# Create your views here.
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
            
            generated_token = base64.b64encode(username)
            confirm_link = reverse('confirm-preregistration-dummy')
            confirm_link += generated_token
            
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
        username = base64.b64decode(confirmation_token)

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

    # Get Recommendation forms for this application period
    try:
        recommendation_forms = RecommendationForm.objects.filter(application_period_id = application_period.pk, sent_by_id = current_user.id)
    
        if len(recommendation_forms) == 0:
            recommendation_forms = None

    except Exception as e:
        recommendation_forms = None
    

    return render(request, 'applicationforms/index.html', {'erdt_form' : erdt_form, 
                                                            'recommendation_forms' : recommendation_forms})


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

    if erdt_form.status == 'In Progress':
        return render(request, 'applicationforms/erdt_form.html', {'form' : form})
    else:
        index(request)

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

    print "ERDT Form last modified date: %s" % erdt_form.last_modified_date    
    erdt_form.last_modified_date = datetime.datetime.now() 
    edited_erdt_form = forms.ERDTFormApplicationForm(request.POST, instance = erdt_form)
    
    if edited_erdt_form.is_valid():
        saved_erdt_form = edited_erdt_form.save()
        print "ERDT Form last modified date saved: %s" % saved_erdt_form.last_modified_date     
        print "ERDT Form id saved: %d" % saved_erdt_form.id
    else:

        return edit_erdt_form(request)

    return index(request)