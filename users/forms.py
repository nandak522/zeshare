from django import forms
from users.models import UserProfile

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput())
    next_url = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput())
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            UserProfile.objects.get(email=email)
            raise forms.ValidationError("Email-id already taken! Please pick a different email")
        except UserProfile.DoesNotExist:
            return email
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput())
    next_url = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput())
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            UserProfile.objects.get(email=email)
            return email
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("Invalid Email and/or Password")