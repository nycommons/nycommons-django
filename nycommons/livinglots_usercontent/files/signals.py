from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import File
from ..signals import add_inplace_action


@receiver(post_save, sender=File, dispatch_uid='activity_stream.file')
def add_file_action(sender, instance=None, **kwargs):
    if not instance: return
    add_inplace_action(instance.added_by, 'posted a file', instance=instance,
                       **kwargs)
