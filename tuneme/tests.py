from django.test import TestCase, RequestFactory
from tuneme.context_processors import default_forms
from tuneme.forms import LoginForm, RegistrationForm, EditProfileForm
from tuneme.forms import ProfilePasswordChangeForm


class ContextProcessorsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_default_forms(self):
        request = self.factory.get('/profiles/login/')
        result = default_forms(request)
        self.assertTrue(
            isinstance(result['login_form'], LoginForm))
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
