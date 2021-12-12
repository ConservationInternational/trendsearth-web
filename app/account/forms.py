from account import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import (User)


class LoginForm(forms.Form):
    """user login form
    """
    email = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(UserCreationForm):
    """user sign up form
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
        self.fields['username'].required = False


class AoiForm(forms.ModelForm):
    """The area of interest form"""
    class Meta:
        model = models.Aoi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].required = False
        self.fields['region'].required = False
        self.fields['city'].required = False
        self.fields['date_created'].required = False


class PasswordResetForm(forms.Form):
    """Password reset form"""
    email = forms.CharField(widget=forms.TextInput)


class SettingsForm(forms.ModelForm):
    """Settings form"""
    can_email_result = forms.BooleanField(
        widget=forms.CheckboxInput,
        initial=True,
        label='Do you want to be notified when execution is finished?',
    )
    in_mail_list = forms.BooleanField(
        widget=forms.CheckboxInput,
        initial=True,
        label='Do you want to be added to our mailing list?',
    )
    update_frequency_milliseconds = forms.IntegerField(
        min_value=1000,
        widget=forms.NumberInput,
        initial=10000,
        label='Specify the refresh frequency (default every 10 seconds)',
    )
    buffer_checked = forms.BooleanField(
        widget=forms.CheckboxInput,
        initial=True,
        label='Do you want buffer to be applied in your area of interest?',
    )
    buffer_size = forms.FloatField(
        widget=forms.NumberInput,
        initial=10.0,
        label='Specify your default buffer size (default 10 kilometers)',
    )
    data_age_limit = forms.IntegerField(
        min_value=1,
        max_value=21,
        initial=14,
        widget=forms.NumberInput,
        label='Specify how long you would want us to keep your results (max 21 days)',
    )

    class Meta:
        model = models.Settings
        fields = ('can_email_result',
                  'in_mail_list', 'update_frequency_milliseconds',
                  'buffer_checked', 'buffer_size',
                  'data_age_limit', 'data_age_limit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['can_email_result'].required = False
        self.fields['in_mail_list'].required = False
        self.fields['buffer_checked'].required = False
