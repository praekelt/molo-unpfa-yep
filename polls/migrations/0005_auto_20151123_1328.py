# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20151123_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.ManyToManyField(related_name='set_vote', null=True, to='polls.PollVote', blank=True),
        ),
    ]
