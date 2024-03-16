# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2024-03-16 22:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewpathways', '0005_reviewpathway_only_urban_renewal_lots'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewpathway',
            name='demolition_completed',
            field=models.BooleanField(default=False, verbose_name=b'Demolition Completed'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='demolition_proposed',
            field=models.BooleanField(default=False, verbose_name=b'Demolition Proposed'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='new_public_housing_built',
            field=models.BooleanField(default=False, verbose_name=b'New Public Housing Built Since 1998'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='new_public_housing_planned',
            field=models.BooleanField(default=False, verbose_name=b'New Public Housing Planned Since 1998'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='nycha_modernization_complete',
            field=models.BooleanField(default=False, verbose_name=b'NYCHA Completed Modernization'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='nycha_modernization_planned',
            field=models.BooleanField(default=False, verbose_name=b'NYCHA-managed Modernization Planned'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='preservation_trust_complete',
            field=models.BooleanField(default=False, verbose_name=b'Preservation Trust Conversion Complete'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='preservation_trust_voting_planned',
            field=models.BooleanField(default=False, verbose_name=b'Voting Planned for Preservation Trust Section 8 Conversion'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='private_infill_planned',
            field=models.BooleanField(default=False, verbose_name=b'Private Infill Planned'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='radpact_converted',
            field=models.BooleanField(default=False, verbose_name=b'RAD/PACT - Converted to Section 8 Under Private Management'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='radpact_planned',
            field=models.BooleanField(default=False, verbose_name=b'Planned RAD/PACT - Section 8 Conversion Under Private Management'),
        ),
        migrations.AddField(
            model_name='reviewpathway',
            name='section_8_pre_2014',
            field=models.BooleanField(default=False, verbose_name=b'Conversions to Section 8 Completed Prior to 2014'),
        ),
    ]
