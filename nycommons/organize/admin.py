from django.contrib import admin

from livinglots_organize.admin import BaseOrganizerAdmin

from .models import Organizer


class OrganizerAdmin(BaseOrganizerAdmin):
    
    def has_add_permission(self, request):
        """Never allow adding organizer through the admin site."""
        return False


admin.site.register(Organizer, OrganizerAdmin)
