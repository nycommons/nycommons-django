# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0015_auto_20170524_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='is_waterfront',
            field=models.BooleanField(default=False),
        ),
    ]