from django.db import migrations, models

from base.utils import Migration


class Migration(Migration):

    dependencies = [
        ('notes', '0002_auto_20150312_1146'),
    ]

    # NB: Depends on base.utils.Migration to migrate another app
    migrated_app = 'notes'

    operations = [
        migrations.AddField(
            model_name='note',
            name='remote',
            field=models.BooleanField(default=False, help_text='Is this from a remote site?'),
        ),
        migrations.AddField(
            model_name='note',
            name='remote_locked',
            field=models.BooleanField(default=False, help_text='When refreshing from the remote site, can we update this one?'),
        ),
        migrations.AddField(
            model_name='note',
            name='remote_pk',
            field=models.PositiveIntegerField(blank=True, help_text='What is the id of this on the remote site?', null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='remote_site',
            field=models.CharField(blank=True, help_text='Which remote site is this from?', max_length=50, null=True),
        ),
    ]
