from django import forms
from utils.widgets import Textarea
from utils import language_choices

class AddSnippetForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    explanation = forms.CharField(required=True, max_length=200)
    code = forms.CharField(required=True, widget=forms.Textarea({'rows':'10', 'cols':'50'}))
    public = forms.BooleanField(required=False, initial=True)
    lang = forms.ChoiceField(choices=language_choices, required=True)
    
class SearchSnippetForm(forms.Form):
    query = forms.CharField(required=True, max_length=50)