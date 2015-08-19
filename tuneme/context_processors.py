# from tuneme.forms import LoginForm
from molo.profiles.forms import LoginForm, RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm


def default_forms(request):
    return {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'edit_profile_form': EditProfileForm(),
        'password_change_form': ProfilePasswordChangeForm()
    }
