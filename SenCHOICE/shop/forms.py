from logging import PlaceHolder
from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "Nom d'ulilisateur"}))
    password = forms.CharField(max_length=63,label='', widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe"}))

class SignupForm(UserCreationForm):
    # username = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "Nom d'ulilisateur"}))
    # email = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "email"}))
    # first_name = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "fist name"}))
    # last_name = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "last name"}))
    # adresse=forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "adresse"}))
    # ville = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "ville"}))
    # pays = forms.CharField(max_length=63, label='',widget=forms.TextInput(attrs={'placeholder': "pays"}))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name','adresse', 'ville', 'pays')
        fields.__class__("block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40")
        
        
       