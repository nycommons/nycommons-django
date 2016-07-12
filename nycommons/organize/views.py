from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from livinglots import get_organizer_model
from livinglots_organize.forms import OrganizerForm
from livinglots_organize.views import AddParticipantView
from lots.models import Lot


class AddOrganizerView(LoginRequiredMixin, PermissionRequiredMixin,
        AddParticipantView):
    content_type_model = Lot
    form_class = OrganizerForm
    login_url = '/admin/login/'
    model=get_organizer_model()
    permission_required = 'organize.add_organizer'
