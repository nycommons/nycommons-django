# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequentlyAskedQuestion',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('articles.article',),
        ),
    ]
