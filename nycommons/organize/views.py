from django.contrib import messages

from livinglots import get_organizer_model
from livinglots_organize.models import OrganizerType
from livinglots_organize.views import AddParticipantView
from lots.models import Lot
from .forms import OrganizerForm, SubscribeForm


class AddOrganizerView(AddParticipantView):
    content_type_model = Lot
    form_class = OrganizerForm
    model=get_organizer_model()


class SubscribeView(AddParticipantView):
    content_type_model = Lot
    form_class = SubscribeForm
    model = get_organizer_model()
    template_name = 'livinglots/organize/subscribe.html'

    def get_initial(self):
        return {
            'post_publicly': False,
            'type': OrganizerType.objects.get(name='individual'),
        }

    def get_success_url(self):
        messages.success(self.request, "Success! You're now subscribed to this lot and will receive updates about it.")
        return self.object.content_object.get_absolute_url()

    def get_template_names(self):
        return [self.template_name,]
