from django.test import TestCase, RequestFactory
from tuneme.context_processors import default_forms


class ContextProcessorsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_default_forms(self):
        request = self.factory.get('/profiles/login/')
        result = default_forms(request)
        assert(result['login_form'])
