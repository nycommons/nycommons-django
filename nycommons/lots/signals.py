from django.db.models.signals import post_save
from django.dispatch import receiver

from organize.models import Organizer


@receiver(post_save, sender=Organizer, dispatch_uid='lot_update_organizing')
def update_organizing(sender, instance, **kwargs):
    """
    Once a Organizer is moderated and approved, track that on the lot.
    """
    if not instance:
        return

    lot = instance.content_object
    lot.organizing = True
    lot.save()
