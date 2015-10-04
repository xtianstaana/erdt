from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from applicationforms import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from profiling.models import *
import base64
import sys
from django.conf import settings
from django.core.mail import EmailMessage

# Create your views here.
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

            # Create profile
            profile = Profile(role = 'REGISTRANT', person = person)

            # Send email
            body = ("Dear %s %s \n" % (firstname, lastname))
            
            generated_token = base64.b64encode(username)
            confirm_link = reverse('confirm-preregistration')
            confirm_link += generated_token
            
            body += "Confirmation link: %s" % (request.build_absolute_uri(confirm_link))

            print body
            
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
    # To be done: complete this method
    return HttpResponse("Your token: %s" % confirmation_token)
