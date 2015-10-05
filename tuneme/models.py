from molo.core.models import ArticlePage
from django_comments.moderation import moderator
from django_comments.moderation import CommentModerator


class ArticleModerator(CommentModerator):
    def allow(self, comment, content_object, request):
        return content_object.allow_commenting()

moderator.register(ArticlePage, ArticleModerator)
