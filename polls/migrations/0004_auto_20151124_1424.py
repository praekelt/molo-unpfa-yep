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
                ('choice', models.ForeignKey(to='polls.Choice')),
                ('question', models.ForeignKey(to='polls.Question')),
                ('user', models.ForeignKey(related_name='poll_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='pollVotes',
            field=models.ManyToManyField(related_name='set_vote', null=True, to='polls.PollVote', blank=True),
        ),
    ]
