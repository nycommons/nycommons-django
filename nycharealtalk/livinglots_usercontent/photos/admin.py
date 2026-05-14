from django.contrib import admin

from imagekit.admin import AdminThumbnail

from ..admin import BaseUserContentAdmin
from .models import Photo


class PhotoAdmin(BaseUserContentAdmin):
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    list_display = ('pk', 'name', 'admin_thumbnail', 'added_by_name', 'added',
                    'linked_target',)
    search_fields = ('name', 'added_by_name',)


admin.site.register(Photo, PhotoAdmin)
