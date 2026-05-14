# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='added_by_name',
            field=models.CharField(max_length=256, null=True, verbose_name='added by name', blank=True),
            preserve_default=True,
        ),
    ]
