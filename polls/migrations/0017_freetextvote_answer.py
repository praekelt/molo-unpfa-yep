# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20151215_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='freetextvote',
            name='answer',
            field=models.TextField(null=True, blank=True),
        ),
    ]
