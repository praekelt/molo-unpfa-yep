from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from molo.core.models import HomePage

HomePage.subpage_types += ['polls.Question']


class Question(Page):
    parent_page_types = [
        'core.LanguagePage', 'core.SectionPage', 'core.ArticlePage']
    subpage_types = ['polls.Choice']

    def choices(self):
        return Choice.objects.live().child_of(self)


class Choice(Page):
    votes = models.IntegerField(default=0)

    promote_panels = Page.promote_panels + [
        FieldPanel('votes'),
    ]
