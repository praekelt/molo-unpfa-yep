from django.utils.translation import ugettext_lazy as _
from molo.core.models import ArticlePage
from molo.yourwords.models import YourWordsCompetitionEntry

from django_comments.moderation import moderator
from django_comments.moderation import CommentModerator

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel)


class ArticleModerator(CommentModerator):
    def allow(self, comment, content_object, request):
        return content_object.allow_commenting()


moderator.register(ArticlePage, ArticleModerator)

# Monkey patch your YourWordsCompetitionEntry panels
YourWordsCompetitionEntry.panels = [
    MultiFieldPanel(
        [
            FieldPanel('competition'),
            FieldPanel('story_name'),
            FieldPanel('user'),
            FieldPanel('story_text'),
            FieldPanel('is_read'),
            FieldPanel('is_shortlisted'),
            FieldPanel('is_winner'),
        ],
        heading=_("Entry Settings"),)
]
