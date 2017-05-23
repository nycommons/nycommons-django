# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0013_auto_20160823_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='commons_type',
            field=models.CharField(choices=[(b'library', b'library'), (b'park', b'park'), (b'post office', b'post office'), (b'public housing', b'public housing'), (b'vacant lot / garden', b'vacant lot / garden'), (b'waterfront', b'waterfront')], max_length=25),
        ),
    ]