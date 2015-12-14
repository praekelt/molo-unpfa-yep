# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20151211_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='show_results',
            field=models.BooleanField(default=True, help_text='This option allows the users to see the results'),
        ),
    ]
