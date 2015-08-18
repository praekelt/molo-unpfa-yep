from django import forms
from molo.profiles import forms as profile_forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Username'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('4 Digit PIN'),
    }))


class RegistrationForm(profile_forms.RegistrationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Username'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('4 Digit PIN'),
    }))


class EditProfileForm(profile_forms.EditProfileForm):
    alias = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Display Name'),
    }))


class ProfilePasswordChangeForm(profile_forms.ProfilePasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Old Password'),
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('New Password'),
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Confirm Password'),
    }))
