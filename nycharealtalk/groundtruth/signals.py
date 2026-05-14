from .models import GroundtruthRecord

from django.dispatch import receiver
from django_monitor import post_moderation

from livinglots_notify.helpers import notify_facilitators


@receiver(post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord_notify')
def notify(sender, instance=None, **kwargs):
    """
    Notify facilitators
    """
    if not instance:
        return
    notify_facilitators(instance)


@receiver(post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord')
def update_use(sender, instance, **kwargs):
    """
    Once a GroundtruthRecord is moderated and approved, make it official by
    updating the use on the referred-to Lot.
    """
    if not instance.is_approved or not instance.content_object:
        return

    lot = instance.content_object

    lot.known_use = instance.use
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.save()
