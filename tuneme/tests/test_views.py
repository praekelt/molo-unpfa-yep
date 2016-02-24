from datetime import datetime
from bs4 import BeautifulSoup
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import ArticlePage
from molo.commenting.models import MoloComment
from molo.commenting.forms import MoloCommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site


class ViewsTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

    def create_comment(self, article, comment, parent=None):
        return MoloComment.objects.create(
            content_type=ContentType.objects.get_for_model(article),
            object_pk=article.pk,
            content_object=article,
            site=Site.objects.get_current(),
            user=self.user,
            comment=comment,
            parent=parent,
            submit_date=datetime.now())

    def test_default_dob_in_registration_done(self):
        client = Client()
        client.login(username='tester', password='tester')
        response = client.get(reverse('registration_done'))

        year_25_ago = datetime.today().year - 25
        self.assertContains(
            response,
            '<option value="%(year)s" selected="selected">%(year)s</option>' %
            {'year': year_25_ago})

    def test_report_response(self):
        client = Client()
        article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1])
        comment = MoloComment.objects.create(
            content_object=article, object_pk=article.id,
            content_type=ContentType.objects.get_for_model(article),
            site=Site.objects.get_current(), user=self.user,
            comment='comment 1', submit_date=datetime.now())
        response = client.get(reverse('report_response',
                                      args=(comment.id,)))
        self.assertContains(
            response,
            "This comment has been reported."
        )

    def test_commenting_closed(self):
        client = Client()
        client.login(username='tester', password='tester')
        article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1], commenting_state='C')
        article.save()
        initial = {
            'object_pk': article.id,
            'content_type': "core.articlepage"
        }
        data = MoloCommentForm(article, {},
                               initial=initial).generate_security_data()
        data.update({
            'comment': "This is another comment"
        })
        response = client.post(reverse('molo-comments-post'), data)
        self.assertEqual(response.status_code, 400)

    def test_commenting_open(self):
        client = Client()
        client.login(username='tester', password='tester')
        article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1], commenting_state='O')
        article.save()
        initial = {
            'object_pk': article.id,
            'content_type': "core.articlepage"
        }
        data = MoloCommentForm(article, {},
                               initial=initial).generate_security_data()
        data.update({
            'comment': "This is a second comment",
        })
        response = client.post(reverse('molo-comments-post'), data)
        self.assertEqual(response.status_code, 302)

    def test_comment_reply(self):
        article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1], commenting_state='O')
        article.save()

        comment1 = self.create_comment(article, 'test comment1 text')
        comment2 = self.create_comment(article, 'test comment2 text')
        comment3 = self.create_comment(article, 'test comment3 text')
        reply = self.create_comment(article,
                                    'test reply text', parent=comment2)
        response = self.client.get(
            reverse('more-comments', args=(article.pk,)))

        html = BeautifulSoup(response.content, 'html.parser')
        [c3row, c2row, replyrow, c1row] = html.find_all(class_='comment')
        self.assertTrue(comment3.comment in c3row.prettify())
        self.assertTrue(comment2.comment in c2row.prettify())
        self.assertTrue(reply.comment in replyrow.prettify())
        self.assertTrue(comment1.comment in c1row.prettify())

    def test_comment_reply_in_article(self):
            self.mk_main()
            self.yourmind = self.mk_section(
                self.main, title='Your mind')
            article = self.mk_article(self.yourmind, title='article 1',
                                      subtitle='article 1 subtitle',
                                      slug='article-1')

            comment1 = self.create_comment(article, 'test comment1 text')
            comment2 = self.create_comment(article, 'test comment2 text')
            comment3 = self.create_comment(article, 'test comment3 text')
            reply = self.create_comment(article,
                                        'test reply text', parent=comment2)
            response = self.client.get('/your-mind/article-1/')
            print response
            html = BeautifulSoup(response.content, 'html.parser')
            [c3row, c2row, replyrow, c1row] = html.find_all(class_='comment')
            self.assertTrue(comment3.comment in c3row.prettify())
            self.assertTrue(comment2.comment in c2row.prettify())
            self.assertTrue(reply.comment in replyrow.prettify())
            self.assertTrue(comment1.comment in c1row.prettify())
