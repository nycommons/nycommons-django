from django.contrib import admin

from livinglots_groundtruth.admin import GroundtruthRecordAdminMixin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(GroundtruthRecordAdminMixin, admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(GroundtruthRecordAdmin, self).__init__(*args, **kwargs)
        self.fields += ('use',)


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
