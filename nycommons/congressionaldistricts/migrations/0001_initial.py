# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2024-03-16 22:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boundaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CongressMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='boundaries.Boundary', verbose_name='district')),
            ],
        ),
    ]