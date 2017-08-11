# -*- coding: UTF-8 -*-
from django.core.management import call_command
from django.utils.six import StringIO
from django.test import TestCase
from django.test.client import Client


from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import (
    SiteLanguageRelation, Main, Languages, LanguageRelation, SiteLanguage)

from wagtail.wagtailcore.models import Page


class CommandsTestCase(TestCase, MoloTestCaseMixin):

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
        self.section = self.mk_section(
            self.section_index, title='test section')
        self.article = self.mk_article(
            self.section,
            title='article 1')

    def test_linking_pages_to_main_language(self):
        # test that when deleting a site langauge, it delets the language
        # relations
        self.assertContains(self.client.get('/'), self.section.title)
        self.assertNotEquals(LanguageRelation.objects.all().count(), 0)
        SiteLanguage.objects.all().delete()
        self.assertEquals(LanguageRelation.objects.all().count(), 0)
        self.assertNotContains(self.client.get('/'), self.section.title)

        # create new english
        english2 = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)
        out = StringIO()
        call_command('link_content_to_main_language', stdout=out)

        # test that the new relation was created and that content displays
        self.assertContains(self.client.get('/'), self.section.title)
        self.assertEquals(
            LanguageRelation.objects.all().count(),
            Page.objects.descendant_of(self.main).count())

        for relation in LanguageRelation.objects.all():
            self.assertEquals(relation.language.pk, english2.pk)
