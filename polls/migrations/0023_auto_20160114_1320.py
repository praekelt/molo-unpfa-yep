# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_auto_20160114_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='short_name',
            field=models.TextField(help_text=b"The short name will replace the title when downloading your results. e.g '10 years old' would be replaced by '10' in the title column.", null=True, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='extra_style_hints',
            field=models.TextField(default=b'', help_text='Styling options that can be applied to this section and all its descendants', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='short_name',
            field=models.TextField(help_text=b"The short name will replace the title when downloading your results. e.g 'How old are you' would be replaced by 'Age' in the title column.", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='show_results',
            field=models.BooleanField(default=True, help_text='This option allows the users to see the results.'),
        ),
    ]
