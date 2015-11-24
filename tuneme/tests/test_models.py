from polls.models import Choice, Question
from polls.views import vote
from django.test import TestCase
from django.contrib.auth.models import User
from molo.core.models import LanguagePage, Main
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Site, Page
from django.http import HttpRequest


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')
        # Create page content type
        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Create root page
        Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )

        main_content_type, created = ContentType.objects.get_or_create(
            model='main', app_label='core')

        # Create a new homepage
        main = Main.objects.create(
            title="Main",
            slug='main',
            content_type=main_content_type,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )
        main.save_revision().publish()

        self.english = LanguagePage(
            title='English',
            code='en',
            slug='english')
        main.add_child(instance=self.english)
        self.english.save_revision().publish()

        # Create a site with the new homepage set as the root
        Site.objects.all().delete()
        Site.objects.create(
            hostname='localhost', root_page=main, is_default_site=True)

    def test_poll_vote(self):
        # make choices
        choice1 = Choice(title='yes', depth=2)
        # make a question
        question = Question.objects.create(title='is this a test', depth=1)
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        # make a vote
        request = HttpRequest()
        request.POST['choice'] = choice1
        vote(request, question.id)
        # should automatically create the poll vote
        # test poll vote
        self.assertEquals(choice1.votes, 1)
