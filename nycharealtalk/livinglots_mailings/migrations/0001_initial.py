# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.BooleanField(default=False, help_text='The mailing was sent', verbose_name='sent')),
                ('recorded', models.DateTimeField(help_text='When this mailing was recorded', verbose_name='recorded', auto_now_add=True)),
                ('receiver_object_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('duplicate_handling', models.CharField(default=b'each', help_text='How should we handle mailings that are going to go to the same email address multiple times?', max_length=32, verbose_name='duplicate handling', choices=[(b'each', b'send each'), (b'first', b'send first'), (b'merge', b'merge')])),
                ('subject_template_name', models.CharField(help_text='The path to the template to use when building the mailing subject line', max_length=256, verbose_name='subject template name')),
                ('text_template_name', models.CharField(help_text='The path to the template to use when building the mailing text line', max_length=256, verbose_name='text template name')),
                ('last_checked', models.DateTimeField(help_text='The last time this mailing was sent.', verbose_name='last checked')),
                ('target_types', models.ManyToManyField(help_text='The types this mailing will be sent to', to='contenttypes.ContentType', verbose_name='target types')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deliveryrecord',
            name='mailing',
            field=models.ForeignKey(help_text='The mailing that was sent', to='livinglots_mailings.Mailing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliveryrecord',
            name='receiver_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
