from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


 
class ContactForm(forms.Form): 
    email = forms.EmailField(required=True, 
        error_messages={'required': '* Please give an email address', 'invalid': '* Please enter a valid e-mail address.'})
    name = forms.CharField(max_length=200, required=True, error_messages={'required': '* Please give your name!'})
    message = forms.CharField(widget=forms.Textarea, required=True, 
        error_messages={'required': '* Please write a message!'})
