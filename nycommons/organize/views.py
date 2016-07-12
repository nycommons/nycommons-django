from django.contrib import messages

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from livinglots import get_organizer_model, get_watcher_model
from livinglots_organize.forms import OrganizerForm
from livinglots_organize.views import AddParticipantView
from lots.models import Lot
from .forms import WatcherForm


class AddOrganizerView(LoginRequiredMixin, PermissionRequiredMixin,
        AddParticipantView):
    content_type_model = Lot
    form_class = OrganizerForm
    login_url = '/admin/login/'
    model=get_organizer_model()
    permission_required = 'organize.add_organizer'


class SubscribeView(AddParticipantView):
    content_type_model = Lot
    form_class = WatcherForm
    model = get_watcher_model()
    template_name = 'livinglots/organize/subscribe.html'

    def get_success_url(self):
        messages.success(self.request, "Success! You're now subscribed to this lot and will receive updates about it.")
        return self.object.content_object.get_absolute_url()

    def get_template_names(self):
        return [self.template_name,]
