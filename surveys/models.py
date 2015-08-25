from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index


class Survey(Page):
    survey_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Choose Page")
    )

    def __str__(self):
        return self.survey_text

    search_fields = Page.search_fields + (
        index.SearchField('pub_date'),
        index.SearchField('survey_text'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('page'),
        FieldPanel('pub_date'),
        FieldPanel('survey_text'),
    ]


class Answer(Page):
    survey = models.ForeignKey(
        Survey,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text

    search_fields = Page.search_fields + (
        index.SearchField('answer_text'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('survey'),
        FieldPanel('answer_text'),
    ]
