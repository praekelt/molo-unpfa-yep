# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20151124_1424'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='pollVotes',
            new_name='poll_votes',
        ),
    ]
