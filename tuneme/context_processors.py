from tuneme.forms import LoginForm, RegistrationForm, EditProfileForm
from tuneme.forms import ProfilePasswordChangeForm


def default_forms(request):
    return {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'edit_profile_form': EditProfileForm(),
        'password_change_form': ProfilePasswordChangeForm()
    }
