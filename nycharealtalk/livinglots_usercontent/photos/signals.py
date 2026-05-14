from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Photo
from ..signals import add_inplace_action


@receiver(post_save, sender=Photo, dispatch_uid='activity_stream.photo')
def add_photo_action(sender, instance=None, **kwargs):
    if not instance: return
    add_inplace_action(instance.added_by, 'posted a picture',
                       instance=instance, **kwargs)
