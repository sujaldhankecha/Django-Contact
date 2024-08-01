from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Contact


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email', 'username': 'Username'}

class ContactForm(forms.ModelForm):
     class Meta:
        model = Contact
        fields = ['firstname', 'lastname', 'mobile', 'email','address']
        # widgets = {'firstname':forms.TextInput(attrs={'class':'form-control'}),
        #            'lastname':forms.TextInput(attrs={'class':'form-control'}),
        #            'mobile':forms.TextInput(attrs={'class':'form-control'}),
        #            'email':forms.TextInput(attrs={'class':'form-control'}),
        #            'address':forms.TextInput(attrs={'class':'form-control'}),
        #            }
