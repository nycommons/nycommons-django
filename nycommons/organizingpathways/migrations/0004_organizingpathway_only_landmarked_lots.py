# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizingpathways', '0003_organizingpathway_only_waterfront_lots'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizingpathway',
            name='only_landmarked_lots',
            field=models.BooleanField(default=False),
        ),
    ]