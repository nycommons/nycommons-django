from django.contrib import admin

from livinglots_steward.admin import (StewardNotificationAdminMixin,
                                      StewardProjectAdminMixin)

from .models import StewardNotification, StewardProject


class StewardNotificationAdmin(StewardNotificationAdminMixin, admin.ModelAdmin):
    pass


class StewardProjectAdmin(StewardProjectAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
