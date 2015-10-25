from django import forms
from uni_form.helper import FormHelper
from uni_form.layout import *
from applicationforms.models import *

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


class ERDTFormApplicationForm(forms.ModelForm):

    class Meta:
        model = ERDTForm
        fields = ['scholarship_applied_for', 'program_of_study', 'status']

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Sample Section",
                'scholarship_applied_for', 
                'program_of_study'),
            Fieldset(
                "Form Details",
                HTML("""
                    <p style='color: red;'>If finished, set status to <b>Submitted</b>. Note that you will be unable to edit the form once submitted</p>
                """),
                'status'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        return super(ERDTFormApplicationForm, self).__init__(*args, **kwargs)

