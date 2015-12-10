from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from molo.core.models import HomePage, LanguagePage, ArticlePage

HomePage.subpage_types += ['polls.Question']
LanguagePage.subpage_types += ['polls.Question']
ArticlePage.subpage_types += ['polls.Question']


class Question(Page):
    subpage_types = ['polls.Choice']

    def can_vote(self, user):
        self.choicevote_set.filter(user=user)
        return not (ChoiceVote.objects.filter(
            user=user, question__id=self.id).exists())

    def choices(self):
        return Choice.objects.live().child_of(self).order_by('?')


class Choice(Page):
    votes = models.IntegerField(default=0)
    choice_votes = models.ManyToManyField('ChoiceVote',
                                          related_name='choices',
                                          null=True, blank=True)

    promote_panels = Page.promote_panels + [
        FieldPanel('votes'),
    ]


class ChoiceVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='choice_votes')
    choice = models.ForeignKey('Choice')
    question = models.ForeignKey('Question')
