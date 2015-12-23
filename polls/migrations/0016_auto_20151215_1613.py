# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_freetextquestion_freetextvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextvote',
            name='question',
            field=models.ForeignKey(to='polls.FreeTextQuestion'),
        ),
    ]
