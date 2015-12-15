# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20151214_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='allow_multiple_choice',
            field=models.BooleanField(default=True, help_text='Allows the user to choose more than one option.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='show_results',
            field=models.BooleanField(default=True, help_text='This option allows the users to see the results.'),
        ),
    ]
