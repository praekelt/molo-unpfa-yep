from molo.core.models import ArticlePage
from django.db import models
from django_comments.moderation import moderator
from django_comments.moderation import CommentModerator
from django.db.models.signals import post_save
from notifications.signals import notify


class ArticleModerator(CommentModerator):
    def allow(self, comment, content_object, request):
        return content_object.allow_commenting()

    def save(self, *args, **kwargs):
        notify.send(self.user, recipient=self.content_object.author,
                    action_object=self.content_object, target=self,
                    verb="commented on")

moderator.register(ArticlePage, ArticleModerator)


class Person(models.Model):
    name = models.CharField(max_length=255)


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was saved')

post_save.connect(my_handler, sender=Person)
