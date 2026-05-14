from django.contrib import admin

from ..admin import BaseUserContentAdmin
from .models import Note


class NoteAdmin(BaseUserContentAdmin):
    list_display = ('added_by_name', 'text', 'added', 'linked_target',)
    search_fields = ('text', 'added_by_name',)

    try:
        import django_wysiwyg

        change_form_template = 'notes/admin/change_form.html'
    except ImportError:
        pass


admin.site.register(Note, NoteAdmin)
