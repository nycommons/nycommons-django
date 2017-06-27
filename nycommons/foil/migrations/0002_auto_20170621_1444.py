# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foilcontact',
            name='appeal_officer_email',
            field=models.EmailField(blank=True, help_text='The email of the FOIL appeal officer', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='foilcontact',
            name='appeal_officer_name',
            field=models.CharField(blank=True, help_text='The name of the FOIL appeal officer', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='foilcontact',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='foilcontact',
            name='officer_email',
            field=models.EmailField(blank=True, help_text='The email of the FOIL officer', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='foilcontact',
            name='officer_name',
            field=models.CharField(blank=True, help_text='The name of the FOIL officer', max_length=300, null=True),
        ),
    ]