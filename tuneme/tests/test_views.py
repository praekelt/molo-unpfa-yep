from datetime import datetime
from bs4 import BeautifulSoup

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import SiteLanguageRelation, Main, Languages
from molo.commenting.models import MoloComment
from molo.commenting.forms import MoloCommentForm


class ViewsTestCase(TestCase, MoloTestCaseMixin):

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

        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')
        self.section = self.mk_section(
            self.section_index, title='test section')
        self.article = self.mk_article(
            self.section,
            title='article 1')

    def create_comment(self, article, comment, parent=None):
        return MoloComment.objects.create(
            content_type=ContentType.objects.get_for_model(article),
            object_pk=article.pk,
            content_object=article,
            site=Site.objects.get_current(),
            user=self.user,
            comment=comment,
            parent=None,
            submit_date=datetime.now())

    def test_default_dob_in_registration_done(self):
        self.client.login(username='tester', password='tester')
        response = self.client.get(reverse('registration_done'))

        year_25_ago = datetime.today().year - 25
        self.assertContains(
            response,
            '<option value="%(year)s" selected="selected">%(year)s</option>' %
            {'year': year_25_ago})

    def test_report_response(self):
        comment = self.create_comment(self.article, 'test comment 1')
        response = self.client.get(reverse('report_response',
                                           args=(comment.id,)))
        self.assertContains(
            response,
            "This comment has been reported."
        )

    def test_commenting_closed(self):
        self.client.login(username='tester', password='tester')
        article = self.mk_article(self.section, commenting_state='C')
        initial = {
            'object_pk': article.id,
            'content_type': "core.articlepage"
        }
        data = MoloCommentForm(article, {},
                               initial=initial).generate_security_data()
        data.update({
            'comment': "This is another comment"
        })
        response = self.client.post(
            reverse('molo.commenting:molo-comments-post'), data)
        self.assertEqual(response.status_code, 400)

    def test_commenting_open(self):
        self.client.login(username='tester', password='tester')
        article = self.mk_article(self.section, commenting_state='O')
        initial = {
            'object_pk': article.id,
            'content_type': "core.articlepage"
        }
        data = MoloCommentForm(article, {},
                               initial=initial).generate_security_data()
        data.update({
            'comment': "This is a second comment",
        })
        response = self.client.post(
            reverse('molo.commenting:molo-comments-post'), data)
        self.assertEqual(response.status_code, 302)

    def test_comment_reply(self):
        article = self.mk_article(self.section, commenting_state='O')

        comment1 = self.create_comment(article, 'test comment1 text')
        comment2 = self.create_comment(article, 'test comment2 text')
        comment3 = self.create_comment(article, 'test comment3 text')
        reply = self.create_comment(article,
                                    'test reply text', parent=comment2)
        response = self.client.get(
            reverse('molo.commenting:more-comments', args=(article.pk,)))
        html = BeautifulSoup(response.content, 'html.parser')

        html.find_all(
            class_='comment-list__item')

        [c3row, c2row, replyrow, c1row] = html.find_all(
            class_='comment-list__item')
        # print(c3row)
        self.assertTrue(comment3.comment in c3row.prettify())
        self.assertTrue(comment2.comment in c2row.prettify())
        self.assertTrue(reply.comment in replyrow.prettify())
        self.assertTrue(comment1.comment in c1row.prettify())

    def test_service_directory_link_enabled(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Find a service')

        with self.settings(ENABLE_SERVICE_DIRECTORY=True):
            response = self.client.get('/')
            self.assertContains(response, 'Find a service')

    def test_KKKKKomment_reply_in_artile(self):
            self.yourmind = self.mk_section(
                self.section_index, title='Your mind')
            article = article = self.mk_article(
                self.section, commenting_state='O')
            comment1 = self.create_comment(article, 'test comment1 text')
            comment2 = self.create_comment(article, 'test comment2 text')
            comment3 = self.create_comment(article, 'test comment3 text')
            reply = self.create_comment(article,
                                        'test reply text', parent=comment2)
            response = self.client.get(article.url)
            html = BeautifulSoup(response.content, 'html.parser')
            [c3row, c2row, replyrow, c1row] = html.find_all(
                class_='comment-list__item')
            self.assertTrue(comment3.comment in c3row.prettify())
            self.assertTrue(comment2.comment in c2row.prettify())
            self.assertTrue(reply.comment in replyrow.prettify())
            self.assertTrue(comment1.comment in c1row.prettify())

    def test_comment_shows_user_display_name(self):
        self.yourmind = self.mk_section(
            self.section_index, title='Your mind')
        article = self.mk_article(self.yourmind, title='article 1',
                                  subtitle='article 1 subtitle',
                                  slug='article-1')

        # check when user doesn't have an alias
        self.create_comment(article, 'test comment1 text')
        response = self.client.get('/sections/your-mind/article-1/')
        self.assertContains(response, "Anonymous")

        # check when user have an alias
        self.user.profile.alias = 'this is my alias'
        self.user.profile.save()
        self.create_comment(article, 'test comment2 text')
        response = self.client.get('/sections/your-mind/article-1/')
        self.assertContains(response, "this is my alias")
        self.assertNotContains(response, "tester")


class TagManagerAccountTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.client = Client()

    def test_gtm_account(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'GTM-XXXXXX')

        with self.settings(GOOGLE_TAG_MANAGER_ACCOUNT='GTM-XXXXXX'):
            response = self.client.get('/')
            self.assertContains(response, 'GTM-XXXXXX')


class TestFrontEndCommentReplies(TestCase, MoloTestCaseMixin):

    def create_comment(self, article, comment, user, parent=None):
        return MoloComment.objects.create(
            content_type=ContentType.objects.get_for_model(article),
            object_pk=article.pk,
            content_object=article,
            site=Site.objects.get_current(),
            user=user,
            comment=comment,
            parent=parent,
            submit_date=datetime.now())

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

        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='password'
        )

        self.moderator_group, _created = Group.objects.get_or_create(
            name='Moderator')
        self.comment_moderator_group, _created = Group.objects.get_or_create(
            name='Comment Moderator')
        self.expert_group, _created = Group.objects.get_or_create(
            name='Expert')

        self.moderator = User.objects.create_user(
            username='moderator',
            email='moderator@example.com',
            password='password',
        )
        self.moderator.groups.set([self.moderator_group])

        self.comment_moderator = User.objects.create_user(
            username='comment_moderator',
            email='comment_moderator@example.com',
            password='password',
        )
        self.comment_moderator.groups.set([self.comment_moderator_group])

        self.expert = User.objects.create_user(
            username='expert',
            email='expert@example.com',
            password='password',
        )
        self.expert.groups.set([self.expert_group])

        # create ordinary user
        self.bob = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='password',
        )

        self.section = self.mk_section(
            self.section_index, title='section')
        self.article = self.mk_article(self.section, title='article 1',
                                       subtitle='article 1 subtitle',
                                       slug='article-1')
        self.comment = self.create_comment(
            article=self.article,
            comment="this_is_comment_content",
            user=self.bob
        )

    def check_reply_exists(self, client):
        response = client.get(
            '/sections/{0}/{1}/'.format(self.section.slug,
                                        self.article.slug)
        )
        self.assertTrue(response.status_code, 200)
        comment_reply_url = ('/commenting/molo/reply/{0}/'
                             .format(self.comment.pk))
        reply_link = '<a href="{0}">Reply</a>'.format(comment_reply_url)
        self.assertContains(response, reply_link, html=True)

        response = self.client.get(comment_reply_url)
        self.assertTrue(response.status_code, 200)

    def test_expert_can_reply_to_comments_on_front_end(self):
        client = Client()
        client.login(
            username=self.expert.username, password='password')
        self.check_reply_exists(client)

        self.bob.profile.alias = 'bob_alias'
        self.bob.profile.save()

        self.check_reply_exists(client)

    def test_moderator_can_reply_to_comments_on_front_end(self):
        client = Client()
        client.login(
            username=self.moderator.username, password='password')
        self.check_reply_exists(client)

        self.bob.profile.alias = 'bob_alias'
        self.bob.profile.save()

        self.check_reply_exists(client)

    def test_comment_moderator_can_reply_to_comments_on_front_end(self):
        client = Client()
        client.login(
            username=self.comment_moderator.username, password='password')
        self.check_reply_exists(client)

        self.bob.profile.alias = 'bob_alias'
        self.bob.profile.save()

        self.check_reply_exists(client)

    def test_superuser_can_reply_to_comments_on_front_end(self):
        client = Client()
        client.login(
            username=self.superuser.username, password='password')
        self.check_reply_exists(client)

        self.bob.profile.alias = 'bob_alias'
        self.bob.profile.save()

        self.check_reply_exists(client)
