from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from molo.core.models import HomePage, LanguagePage, ArticlePage
from django.utils.translation import ugettext_lazy as _

HomePage.subpage_types += ['polls.Question']
LanguagePage.subpage_types += ['polls.Question']
ArticlePage.subpage_types += ['polls.Question']


class Question(Page):
    subpage_types = ['polls.Choice']
    randomise_options = models.BooleanField(
        default=False,
        help_text=_(
            "Randomising the options allows the options to be shown" +
            " in a different order each time the page is displayed."))
    content_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('randomise_options')], heading="Question Settings",)]

    def can_vote(self, user):
        self.choicevote_set.filter(user=user)
        return not (ChoiceVote.objects.filter(
            user=user, question__id=self.id).exists())

    def choices(self):
        if self.randomise_options:
            return Choice.objects.live().child_of(self).order_by('?')
        else:
            return Choice.objects.live().child_of(self)


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
