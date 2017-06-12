from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from molo.core.models import Main, Languages, SiteLanguageRelation
from molo.core.tests.base import MoloTestCaseMixin


class ArticleLoginFlow(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.client = Client()

        self.main = Main.objects.all().first()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)
        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)

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
            '/engilsh/sex/sub-category-4/article/')
