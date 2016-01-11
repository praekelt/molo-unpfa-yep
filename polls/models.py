from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from molo.core.models import HomePage, LanguagePage, ArticlePage
from django.utils.translation import ugettext_lazy as _

HomePage.subpage_types += ['polls.Question', 'polls.FreeTextQuestion']
LanguagePage.subpage_types += ['polls.Question', 'polls.FreeTextQuestion']
ArticlePage.subpage_types += ['polls.Question', 'polls.FreeTextQuestion']


class Question(Page):
    subpage_types = ['polls.Choice']
    show_results = models.BooleanField(
        default=True,
        help_text=_("This option allows the users to see the results.")
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
    allow_multiple_choice = models.BooleanField(
        default=False,
        help_text=_(
            "Allows the user to choose more than one option.")
    )
    content_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('show_results'),
        FieldPanel('randomise_options'),
        FieldPanel('result_as_percentage'),
        FieldPanel('allow_multiple_choice')], heading=_("Question Settings",))]

    def user_choice(self, user):
        self.choicevote_set.filter(user=user)
        return ChoiceVote.objects.get(
            user=user, question__id=self.id).choice

    def can_vote(self, user):
        return not (ChoiceVote.objects.filter(
            user=user, question__id=self.id).exists())

    def choices(self):
        if self.randomise_options:
            return Choice.objects.live().child_of(self).order_by('?')
        else:
            return Choice.objects.live().child_of(self)


class FreeTextQuestion(Question):
    subpage_types = []
    content_panels = Page.content_panels
    numerical = models.BooleanField(
        default=False,
        help_text=_(
            "When selected, this question will allow numerical data only")
    )
    content_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('numerical')], heading=_("Question Settings",))]

    def __init__(self, *args, **kwargs):
        super(FreeTextQuestion, self).__init__(*args, **kwargs)
        self.show_results = False

    def can_vote(self, user):
        return not (FreeTextVote.objects.filter(
            user=user, question__id=self.id).exists())


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
    choice = models.ManyToManyField('Choice', null=True, blank=True)
    question = models.ForeignKey('Question')
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)

    @property
    def answer(self):
        return ','.join(self.choice.all().values_list('title', flat=True))


class FreeTextVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='text_votes')
    question = models.ForeignKey('FreeTextQuestion')
    answer = models.TextField(blank=True, null=True)
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)
