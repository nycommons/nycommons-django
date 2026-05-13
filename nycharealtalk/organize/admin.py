from django.contrib import admin

from livinglots_organize.admin import BaseOrganizerAdmin

from .models import Organizer


class OrganizerAdmin(BaseOrganizerAdmin):
    list_display = ('name', 'email', 'type', 'post_publicly', 'remote', 'added',
                    'linked_target',)
    list_filter = ('added', 'post_publicly', 'remote',)
    readonly_fields = ('added', 'email_hash', 'linked_target',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                ('email', 'phone',),
                'type', 'notes',
                ('url', 'facebook_page',),
                'post_publicly', 'added',
                'linked_target',
                'email_hash',
            )
        }),
        ('Remote', {
            'classes': ('collapse',),
            'fields': (
                'remote',
                'remote_locked',
                ('remote_site', 'remote_pk',),
            ),
        }),
    )

    def has_add_permission(self, request):
        """Never allow adding organizer through the admin site."""
        return False


admin.site.register(Organizer, OrganizerAdmin)
