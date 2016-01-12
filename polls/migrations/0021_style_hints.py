# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20160111_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='extra_style_hints',
            field=models.TextField(default=b'', help_text='Styling options that can be applied to this section and all its descendants', null=True, blank=True),
        ),
    ]
