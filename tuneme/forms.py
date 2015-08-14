from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Username'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Password'),
    }))
