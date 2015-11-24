# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20151123_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='vote_count',
        ),
        migrations.AddField(
            model_name='choice',
            name='pollVotes',
            field=models.ManyToManyField(related_name='set_vote', null=True, to='polls.PollVote', blank=True),
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
