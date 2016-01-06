# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_freetextquestion_numerical'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freetextquestion',
            name='numerical',
            field=models.BooleanField(default=False, help_text='When selected, this question will allow numerical data only'),
        ),
    ]
