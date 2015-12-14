# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20151211_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='result_as_percentage',
            field=models.BooleanField(default=True, help_text='If not checked, the results will be shown as a total instead of a percentage.'),
        ),
        migrations.AddField(
            model_name='question',
            name='show_results',
            field=models.BooleanField(default=True, help_text='This option allows the results to be shown'),
        ),
    ]
