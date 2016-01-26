
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


class UserProfileValidationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_profile_validation(self):

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'wrong username',
            'password': '1234',
        })
        self.assertContains(response,
                            'This value must contain only letters, '
                            'numbers and underscores.')

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'username',
            'password': 'wrong',
        })
        self.assertContains(response,
                            'This value must contain only numbers.')

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'username',
            'password': '12',
        })
        self.assertContains(response,
                            'Ensure this value has at least 4 characters'
                            ' (it has 2).')

        self.user = User.objects.create_user(
            username='tester',
            password='1234')

        response = self.client.post(reverse('molo.profiles:auth_login'), {
            'username': 'wrong',
            'password': '1234',
        })
        self.assertContains(response,
                            'Your username and password does not match.'
                            ' Please try again.')

        response = self.client.post(reverse('molo.profiles:auth_login'), {
            'username': 'tester',
            'password': 'wrong',
        })
        self.assertContains(response,
                            'Your username and password does not match.'
                            ' Please try again.')
