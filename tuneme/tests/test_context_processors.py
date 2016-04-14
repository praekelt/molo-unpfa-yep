from django.test import TestCase, RequestFactory

from tuneme.context_processors import default_forms

from molo.core.tests.base import MoloTestCaseMixin

from molo.profiles.forms import RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm


class ContextProcessorsTest(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.mk_main()

    def test_default_forms(self):
        request = self.factory.get('/profiles/register/')
        result = default_forms(request)
        self.assertTrue(
            isinstance(result['registration_form'], RegistrationForm))
        request = self.factory.get('/profiles/edit/myprofile/')
        result = default_forms(request)
        self.assertTrue(
            isinstance(result['edit_profile_form'], EditProfileForm))
        request = self.factory.get('/profiles/password-reset/')
        result = default_forms(request)
        self.assertTrue(isinstance(result['password_change_form'],
                        ProfilePasswordChangeForm))
