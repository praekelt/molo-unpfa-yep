# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20151214_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicevote',
            name='choice',
        ),
        migrations.AddField(
            model_name='choicevote',
            name='choice',
            field=models.ManyToManyField(to='polls.Choice', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='allow_multiple_choice',
            field=models.BooleanField(default=False, help_text='Allows the user to choose more than one option.'),
        ),
    ]
