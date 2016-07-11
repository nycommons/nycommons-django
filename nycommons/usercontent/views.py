from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from livinglots_usercontent.views import AddContentView

from lots.models import Lot
from .forms import FileForm, NoteForm, PhotoForm


class AddFileView(LoginRequiredMixin, PermissionRequiredMixin, AddContentView):
    content_type_model = Lot
    form_class = FileForm
    login_url = '/admin/login/'
    permission_required = 'files.add_file'


class AddNoteView(LoginRequiredMixin, PermissionRequiredMixin, AddContentView):
    content_type_model = Lot
    form_class = NoteForm
    login_url = '/admin/login/'
    permission_required = 'notes.add_note'


class AddPhotoView(LoginRequiredMixin, PermissionRequiredMixin, AddContentView):
    content_type_model = Lot
    form_class = PhotoForm
    login_url = '/admin/login/'
    permission_required = 'photos.add_photo'
