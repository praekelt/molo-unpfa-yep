# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0014_auto_20151214_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeTextQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='polls.Question')),
            ],
            options={
                'abstract': False,
            },
            bases=('polls.question',),
        ),
        migrations.CreateModel(
            name='FreeTextVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='polls.Question')),
                ('user', models.ForeignKey(related_name='text_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
