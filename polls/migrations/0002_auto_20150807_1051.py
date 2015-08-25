# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0002_add_verbose_names'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('wagtailsearch', '0002_add_verbose_names'),
        ('wagtailcore', '0016_change_page_url_path_to_text_field'),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LanguagePage',
        ),
    ]
