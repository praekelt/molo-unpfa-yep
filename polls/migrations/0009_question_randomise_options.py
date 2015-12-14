# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20151209_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='randomise_options',
            field=models.BooleanField(default=False),
        ),
    ]
