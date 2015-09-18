
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


class ArticleLoginFlow(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_login_flow(self):

        # Create and login user
        self.user = User.objects.create_user(
            username='tester',
            password='tester')

        response = self.client.post(reverse('molo.profiles:auth_login'), {
            'username': 'tester',
            'password': 'tester',
            'next': '/engilsh/sex/sub-category-4/article/'
        })
        # Test that next url is article url
        self.assertEqual(
            response['Location'],
            'http://testserver/engilsh/sex/sub-category-4/article/')
