# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinglots_mailings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysAfterAddedMailing',
            fields=[
                ('mailing_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='livinglots_mailings.Mailing')),
                ('days_after_added', models.IntegerField(help_text='The number of days after an entity is added that they should receive an email.', verbose_name='days after added')),
            ],
            options={
                'abstract': False,
            },
            bases=('livinglots_mailings.mailing', models.Model),
        ),
    ]
