from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Note
from ..signals import add_inplace_action


@receiver(post_save, sender=Note, dispatch_uid='activity_stream.note')
def add_note_action(sender, instance=None, **kwargs):
    if not instance: return
    add_inplace_action(instance.added_by, 'wrote', instance=instance, **kwargs)


try:
    from .markdown import text_to_markdown

    @receiver(pre_save, sender=Note, dispatch_uid='note.to_markdown')
    def to_markdown(sender, instance=None, **kwargs):
        # Only convert notes the first time they're saved
        if not instance or instance.pk: return
        instance.text = text_to_markdown(instance.text)
except ImportError:
    pass
