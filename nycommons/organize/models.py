from django.core.urlresolvers import reverse

from livinglots_organize.models import BaseOrganizer, BaseWatcher


class Organizer(BaseOrganizer):
    pass

class Watcher(BaseWatcher):

    def get_edit_url(self):
        return reverse('organize:edit_participant', kwargs={
            'hash': self.email_hash,
            'pk': self.object_id,
        })


# Require email fields for both Organizer and Watcher instances
Organizer._meta.get_field('email').blank = False
Watcher._meta.get_field('email').blank = False
