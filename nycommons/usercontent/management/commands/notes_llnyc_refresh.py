from django.conf import settings

from livinglots_usercontent.notes.models import Note
from .refresh import UsercontentRefreshCommand


class Command(UsercontentRefreshCommand):
    help = 'Refresh notes data from LLNYC'
    local_model = Note
    remote_site = 'llnyc'
    remote_url = settings.REMOTE_LOTS['llnyc']['api_notes_url']
    remote_object_key = 'notes'

    def object_kwargs(self, note_json, orig=None):
        kwargs = super(Command, self).object_kwargs(note_json, orig=orig)
        kwargs['text'] = note_json['text']
        return kwargs
