import time

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.test.utils import override_settings
from molo.core.tests.base import MoloTestCaseMixin


@override_settings(SESSION_COOKIE_AGE=1)
class GemAutomaticLogoutTest(TestCase, MoloTestCaseMixin):
    """Note that SESSION_SAVE_EVERY_REQUEST must = True for this to work
    """
    def setUp(self):
        self.client = Client()
        self.mk_main()

        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

    def test_session_expires_if_no_activity_within_session_cookie_age(self):
        self.client.login(username='tester', password='tester')

        response = self.client.get('/profiles/view/myprofile/')

        self.assertContains(response, 'Hello tester')
        self.assertContains(response, 'log out')

        # wait for the session to expire
        time.sleep(1)

        response = self.client.get('/profiles/view/myprofile/', follow=True)
        self.assertRedirects(response,
                             '/profiles/login/?next=/profiles/view/myprofile/')
        self.assertNotContains(response, 'Hello tester')
        self.assertNotContains(response, 'log out')
