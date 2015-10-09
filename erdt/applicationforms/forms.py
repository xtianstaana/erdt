from django import forms
from uni_form.helper import FormHelper
from uni_form.layout import *

class PreRegistrationForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=100)
    lastname = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Personal Details",
                'firstname', 
                'lastname'),
            Fieldset(
                "Account Details",
                'username',
                'email',
                'password',
                'confirm_password'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        return super(PreRegistrationForm, self).__init__(*args, **kwargs)