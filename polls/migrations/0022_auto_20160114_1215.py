# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_style_hints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='extra_style_hints',
        ),
        migrations.AddField(
            model_name='question',
            name='short_name',
            field=models.TextField(help_text='The short name is used when downloading the question and answer', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='show_results',
            field=models.BooleanField(default=True, help_text='The short name will be used when downloading the question. For example, Are you unemployed can be saved as unemployed.'),
        ),
    ]
