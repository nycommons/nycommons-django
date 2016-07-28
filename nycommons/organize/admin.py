from django.contrib import admin

from livinglots_organize.admin import BaseOrganizerAdmin, BaseWatcherAdmin

from .models import Organizer, Watcher


class OrganizerAdmin(BaseOrganizerAdmin):
    
    def has_add_permission(self, request):
        """Never allow adding organizer through the admin site."""
        return False


class WatcherAdmin(BaseWatcherAdmin):
    
    def has_add_permission(self, request):
        """Never allow adding watcher through the admin site."""
        return False


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Watcher, WatcherAdmin)
