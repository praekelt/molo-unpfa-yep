# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 10:04
from __future__ import unicode_literals

from django.db import migrations


def add_25_km_as_default(apps, schema_editor):
    model = apps.get_model('core', 'SiteSettings')
    instance = model.objects.first()
    instance.default_service_directory_radius = 25
    instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tuneme', '0004_delete_polls_index_page'),
    ]

    operations = [
        migrations.RunPython(add_25_km_as_default)
    ]
