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

    def test_voting_once_only(self):
        # make choices
        choice1 = Choice(title='yes')
        # make a question
        question = Question(title='is this a test')
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='tester', password='tester')
        response = client.get('/')
        self.assertContains(response, 'is this a test')
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.votes
        self.assertEquals(vote_count, 1)
        self.assertEquals(
            ChoiceVote.objects.all()[0].choice.choice_votes.count(), 1)
        # vote again and test that it does not add to vote_count
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.votes
        self.assertEquals(vote_count, 1)
