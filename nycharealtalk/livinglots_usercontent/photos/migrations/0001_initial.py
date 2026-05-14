# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('original_image', models.ImageField(upload_to=b'photos', verbose_name='original image')),
                ('name', models.CharField(max_length=256, null=True, verbose_name='name', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('added_by_name', models.CharField(max_length=256, null=True, verbose_name='added by name', blank=True)),
                ('added_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
