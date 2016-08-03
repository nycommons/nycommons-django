# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-03 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20160514_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentPostsContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recentpostscontent_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'recent posts',
                'db_table': 'page_page_recentpostscontent',
                'verbose_name': 'recent posts',
                'permissions': [],
            },
        ),
    ]
