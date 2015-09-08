# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150807_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='choice_text',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='page',
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
    ]
