from django.forms import HiddenInput

from livinglots_organize.forms import ParticipantForm, OrganizerForm as BaseOrganizerForm

from .models import Organizer


class OrganizerForm(BaseOrganizerForm):

    class Meta(BaseOrganizerForm.Meta):
        exclude = (
            'added',
            'remote',
            'remote_locked',
            'remote_pk',
            'remote_site',
            'remote_url',
        )


class SubscribeForm(ParticipantForm):

    class Meta:
        exclude = (
            'added',
            'facebook_page',
            'notes',
            'remote',
            'remote_locked',
            'remote_pk',
            'remote_site',
            'remote_url',
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
