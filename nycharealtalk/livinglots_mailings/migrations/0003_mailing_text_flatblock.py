# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatblocks', '__first__'),
        ('livinglots_mailings', '0002_daysafteraddedmailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='text_flatblock',
            field=models.ForeignKey(blank=True, to='flatblocks.FlatBlock', null=True),
            preserve_default=True,
        ),
    ]
