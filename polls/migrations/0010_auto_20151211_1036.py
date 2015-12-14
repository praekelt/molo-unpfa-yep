# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_question_randomise_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='randomise_options',
            field=models.BooleanField(default=False, help_text='Randomising the options allows the options to be shown in a different order each time the page is displayed.'),
        ),
    ]
