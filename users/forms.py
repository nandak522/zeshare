from django import forms

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput())
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput())