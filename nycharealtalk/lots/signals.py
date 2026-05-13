from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from organize.models import Organizer
from .models import Lot


@receiver(post_save, sender=Organizer, dispatch_uid='lot_update_organizing')
def update_organizing(sender, instance, **kwargs):
    """
    Once a Organizer is moderated and approved, track that on the lot.
    """
    if not (instance and instance.post_publicly):
        return

    lot = instance.content_object
    lot.organizing = True
    lot.save()


@receiver(pre_delete, sender=Organizer,
          dispatch_uid='lot_update_organizing_delete')
def update_organizing_delete(sender, instance, **kwargs):
    """
    Once a Organizer is deleted, consider removing organizing status on lot.
    """
    if not instance:
        return

    lot = instance.content_object
    public_organizers = lot.organizers.filter(post_publicly=True)
    if not public_organizers.exclude(pk=instance.pk).exists():
        lot.organizing = False
        lot.save()


@receiver(post_save, sender=Lot, dispatch_uid='lot_update_area')
def update_area(sender, instance, created=False, **kwargs):
    if not (instance and created):
        return
    # Force calculation of area on lot
    instance._area()
