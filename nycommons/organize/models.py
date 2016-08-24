from django.core.urlresolvers import reverse

from livinglots_organize.models import BaseOrganizer

from remote.models import RemoteMixin


class Organizer(RemoteMixin, BaseOrganizer):

    def _remote_url(self):
        pattern = settings.REMOTE_LOTS[self.remote_site]['organizer_permalink_url_pattern']
        return pattern % self.email_hash
    remote_url = property(_remote_url)

    def get_edit_url(self):
        return reverse('organize:edit_participant', kwargs={
            'hash': self.email_hash,
            'pk': self.object_id,
        })


# Require email fields for Organizer instances
Organizer._meta.get_field('email').blank = False
