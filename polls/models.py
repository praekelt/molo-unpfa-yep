from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from molo.core.models import HomePage, LanguagePage, ArticlePage

HomePage.subpage_types += ['polls.Question']
LanguagePage.subpage_types += ['polls.Question']
ArticlePage.subpage_types += ['polls.Question']


class Question(Page):
    subpage_types = ['polls.Choice']

    def choices(self):
        return Choice.objects.live().child_of(self)


class Choice(Page):
    vote_count = models.IntegerField(default=0)
    votes = models.ManyToManyField('PollVote', related_name='set_vote',
                                   null=True, blank=True)

    promote_panels = Page.promote_panels + [
        FieldPanel('vote_count'),
    ]


class PollVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='poll_votes')
    choice = models.ForeignKey('Choice')
    question = models.ForeignKey('Question')
