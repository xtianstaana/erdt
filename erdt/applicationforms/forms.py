from django import forms

class PreRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    firstname = forms.CharField(label='First Name', max_length=100)
    lastname = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)