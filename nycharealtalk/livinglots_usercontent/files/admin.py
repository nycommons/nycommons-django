from django.contrib import admin

from ..admin import BaseUserContentAdmin
from .models import File


class FileAdmin(BaseUserContentAdmin):
    list_display = ('title', 'added_by_name', 'added', 'linked_target',)
    search_fields = ('title', 'description', 'added_by_name',)


admin.site.register(File, FileAdmin)
