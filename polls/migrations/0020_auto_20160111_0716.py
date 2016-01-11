# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_auto_20160106_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicevote',
            name='submission_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='freetextvote',
            name='submission_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
