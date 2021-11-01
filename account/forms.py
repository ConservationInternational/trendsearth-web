from django.db.models import fields
from account import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import (User, Group)


class LoginForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """
    email = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(UserCreationForm):
    """[summary]

    Args:
        UserCreationForm ([type]): [description]
    """
    first_name = forms.CharField(max_length=100, help_text='Last Name',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Username'
                                 }))
    last_name = forms.CharField(max_length=100, help_text='Last Name',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Last Name'
                                }))
    email = forms.EmailField(max_length=150, help_text='Email',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Email'
                             }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].required = False


class UserGroupForm(forms.Form):
    """Creates a user group form

    Args:
        forms ([type]): [description]
    """
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AoiForm(forms.ModelForm):
    """The area of interest form"""
    class Meta:
        model = models.Aoi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['date_created'].required = False
