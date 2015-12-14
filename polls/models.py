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
    show_results = models.BooleanField(
        default=True,
        help_text=_("This option allows the results to be shown")
    )
    randomise_options = models.BooleanField(
        default=False,
        help_text=_(
            "Randomising the options allows the options to be shown" +
            " in a different order each time the page is displayed."))
    result_as_percentage = models.BooleanField(
        default=True,
        help_text=_(
            "If not checked, the results will be shown as a total" +
            " instead of a percentage.")
    )
    content_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('show_results'),
        FieldPanel('randomise_options'),
        FieldPanel('result_as_percentage')], heading="Question Settings",)]

    def user_choice(self, user):
        self.choicevote_set.filter(user=user)
        return ChoiceVote.objects.get(
            user=user, question__id=self.id).choice.title

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
