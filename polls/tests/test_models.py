from polls.models import Choice, Question, ChoiceVote
from django.test import TestCase
from django.contrib.auth.models import User
from molo.core.models import LanguagePage, Main
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Site, Page
from django.test.client import Client
from django.core.urlresolvers import reverse


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
        choice1 = Choice(title='yes')
        # make a question
        question = Question(title='is this a test')
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        # make a vote
        client = Client()
        client.login(username='tester', password='tester')
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.votes
        self.assertEquals(vote_count, 1)

    def test_question_choices(self):
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        choice3 = Choice(title='maybe')
        choice4 = Choice(title='definitely')
        choice5 = Choice(title='idk')

        question = Question(title='is this a test')
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.add_child(instance=choice3)
        question.add_child(instance=choice4)
        question.add_child(instance=choice5)

        choices = question.choices()
        self.assertEqual(choices.get(title='yes'), choice1)
        self.assertEqual(choices.get(title='no'), choice2)
        self.assertEqual(choices.get(title='maybe'), choice3)
        self.assertEqual(choices.get(title='definitley'), choice4)
        self.assertEqual(choices.get(title='idk'), choice5)
