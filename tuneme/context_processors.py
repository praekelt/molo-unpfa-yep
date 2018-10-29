from django.conf import settings
from molo.profiles.forms import RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm
from molo.core.models import SiteSettings


def default_forms(request):
    return {
        'registration_form': RegistrationForm(),
        'edit_profile_form': EditProfileForm(),
        'password_change_form': ProfilePasswordChangeForm()
    }


def add_tag_manager_account(request):
    site_settings = SiteSettings.for_site(request.site)
    return {
        'GOOGLE_TAG_MANAGER_ACCOUNT': (site_settings.ga_tag_manager
                                       or settings.GOOGLE_TAG_MANAGER_ACCOUNT)
    }


def detect_freebasics(request):
    return {
        'is_via_freebasics':
            'Internet.org' in request.META.get('HTTP_VIA', '')
            or 'InternetOrgApp' in request.META.get('HTTP_USER_AGENT', '')
            or 'true' in request.META.get('HTTP_X_IORG_FBS', '')
    }
