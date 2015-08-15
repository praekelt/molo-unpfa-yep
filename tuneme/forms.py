from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Username'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('4 Digit PIN'),
    }))

class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Username'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('4 Digit PIN'),
    }))

class EditProfileForm(forms.Form):
    alias = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Display Name'),
    }))

class ProfilePasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Old Password'),
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('New Password'),
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Confirm Password'),
    }))
