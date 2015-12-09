# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20151209_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_votes',
            field=models.ManyToManyField(related_name='choices', null=True, to='polls.ChoiceVote', blank=True),
        ),
    ]
