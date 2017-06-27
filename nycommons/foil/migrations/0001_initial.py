# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('owners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoilContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('officer_name', models.CharField(help_text='The name of the FOIL officer', max_length=300)),
                ('officer_email', models.EmailField(help_text='The email of the FOIL officer', max_length=254)),
                ('appeal_officer_name', models.CharField(help_text='The name of the FOIL appeal officer', max_length=300)),
                ('appeal_officer_email', models.EmailField(help_text='The email of the FOIL appeal officer', max_length=254)),
                ('notes', models.TextField()),
                ('owner', models.ForeignKey(help_text='The owner (agency) this contact applies to', on_delete=django.db.models.deletion.CASCADE, to='owners.Owner')),
            ],
        ),
    ]