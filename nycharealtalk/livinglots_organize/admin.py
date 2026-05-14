from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import OrganizerType


class ParticipantAdminMixin(object):

    def linked_target(self, organizer):
        if not organizer.content_object:
            return None
        return mark_safe(
            '<a href="%s">%s</a>' % (
                organizer.content_object.get_absolute_url(),
                organizer.content_object,
            )
        )

    linked_target.short_description = 'target'


class BaseOrganizerAdmin(ParticipantAdminMixin, admin.ModelAdmin):
    exclude = ('content_type', 'object_id',)
    list_display = ('name', 'email', 'type', 'post_publicly', 'added',
                    'linked_target',)
    list_filter = ('added', 'post_publicly',)
    readonly_fields = ('added', 'linked_target',)
    search_fields = ('name', 'email', 'phone', 'notes', 'url',)


class BaseWatcherAdmin(ParticipantAdminMixin, admin.ModelAdmin):
    exclude = ('content_type', 'object_id',)
    list_display = ('name', 'email', 'added', 'linked_target',)
    list_filter = ('added',)
    readonly_fields = ('added', 'linked_target',)
    search_fields = ('name', 'email', 'phone',)


class OrganizerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group',)
    search_fields = ('name',)


admin.site.register(OrganizerType, OrganizerTypeAdmin)
