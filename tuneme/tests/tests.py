from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.test.client import Client

from wagtail.wagtailsearch.backends import get_search_backend

from tuneme.context_processors import default_forms
from tuneme.forms import LoginForm

from molo.profiles.forms import RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm
from molo.core.models import ArticlePage


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


class TestSearch(TestCase):

    def test_search(self):
        for a in range(0, 20):
            ArticlePage.objects.create(
                title='article %s' % (a,), depth=a,
                subtitle='article %s subtitle' % (a,),
                slug='article-%s' % (a,), path=[a])

        self.backend = get_search_backend('default')
        self.backend.refresh_index()

        client = Client()
        response = client.get(reverse('search'), {
            'q': 'article'
        })

        self.assertContains(response, 'Page 1 of 2')
        self.assertContains(response, '&rarr;')
        self.assertNotContains(response, '&larr;')

        response = client.get(reverse('search'), {
            'q': 'article',
            'p': '2',
        })
        self.assertContains(response, 'Page 2 of 2')
        self.assertNotContains(response, '&rarr;')
        self.assertContains(response, '&larr;')
