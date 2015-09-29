from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from molo.core.models import ArticlePage
from molo.commenting.models import MoloComment
from molo.commenting.forms import MoloCommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site


class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

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
        data = MoloCommentForm(self.user, {}).generate_security_data()
        data.update({
            'comment': "This is another comment",
            'object_pk': article.id,
            'content_type': "core.articlepage"
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
        data = MoloCommentForm(self.user, {}).generate_security_data()
        data.update({
            'comment': "This is another comment",
            'object_pk': article.id,
            'content_type': "core.articlepage"
        })
        response = client.post(reverse('molo-comments-post'), data)
        print response
        self.assertEqual(response.status_code, 302)
