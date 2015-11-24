# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0003_auto_20150807_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AddField(
            model_name='pollvote',
            name='choice',
            field=models.ForeignKey(to='polls.Choice'),
        ),
        migrations.AddField(
            model_name='pollvote',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
        ),
        migrations.AddField(
            model_name='pollvote',
            name='user',
            field=models.ForeignKey(related_name='poll_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.ManyToManyField(related_name='set_vote', to='polls.PollVote'),
        ),
    ]
