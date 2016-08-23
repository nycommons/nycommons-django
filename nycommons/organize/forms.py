from django.forms import HiddenInput

from livinglots_organize.forms import ParticipantForm

from .models import Organizer


class SubscribeForm(ParticipantForm):

    class Meta:
        exclude = (
            'added',
            'facebook_page',
            'notes',
            'url',
        )
        widgets = {
            'added_by': HiddenInput(),
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
            'post_publicly': HiddenInput(),
            'type': HiddenInput(),
        }
        model = Organizer
