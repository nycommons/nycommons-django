# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownerpathways', '0002_ownerpathway_only_waterfront_lots'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownerpathway',
            name='only_landmarked_lots',
            field=models.BooleanField(default=False),
        ),
    ]
