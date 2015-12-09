# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20151127_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicevote',
            name='user',
            field=models.ForeignKey(related_name='choice_votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
