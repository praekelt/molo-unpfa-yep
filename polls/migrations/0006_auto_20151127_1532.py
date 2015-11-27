# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0005_auto_20151125_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pollvote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='pollvote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='pollvote',
            name='user',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='poll_votes',
        ),
        migrations.DeleteModel(
            name='PollVote',
        ),
        migrations.AddField(
            model_name='choicevote',
            name='choice',
            field=models.ForeignKey(to='polls.Choice'),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='user',
            field=models.ForeignKey(related_name='poll_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_votes',
            field=models.ManyToManyField(related_name='set_vote', null=True, to='polls.ChoiceVote', blank=True),
        ),
    ]
