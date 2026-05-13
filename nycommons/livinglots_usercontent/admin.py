from django.contrib import admin
from django.utils.safestring import mark_safe


class BaseUserContentAdmin(admin.ModelAdmin):
    exclude = ('content_type', 'object_id',)
    list_filter = ('added',)
    readonly_fields = ('added', 'linked_target',)

    def linked_target(self, user_content):
        if not user_content.content_object:
            return None
        return mark_safe(
            '<a href="%s">%s</a>' % (
                user_content.content_object.get_absolute_url(),
                str(user_content.content_object),
            )
        )

    linked_target.short_description = 'target'
