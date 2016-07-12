from django.forms import HiddenInput

from livinglots_organize.forms import ParticipantForm

from .models import Watcher


class WatcherForm(ParticipantForm):

    class Meta:
        exclude = ('added',)
        widgets = {
            'added_by': HiddenInput(),
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }
        model = Watcher
