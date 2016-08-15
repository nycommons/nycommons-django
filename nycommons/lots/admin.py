from django.contrib import admin

from livinglots_lots.admin import BaseLotAdmin

from .models import Lot


class LotAdmin(BaseLotAdmin):
    list_display = ('address_line1', 'city', 'name', 'commons_type',)
    list_filter = ('commons_type', 'added', 'owner',)
    readonly_fields = ('added', 'group', 'stewards_list',)
    fieldsets = (
        (None, {
            'fields': (
                ('bbl', 'name',),
                ('address_line1', 'address_line2', 'city', 'borough',),
                ('state_province', 'postal_code',),
                ('added', 'added_reason',),
                'group',
            ),
        }),
        ('Commons', {
            'fields': (
                'commons_type',
                'priority',
                'development_pending_explanation',
            ),
        }),
        ('Known use', {
            'classes': ('collapse',),
            'fields': ('known_use', 'known_use_certainty', 'known_use_locked',),
        }),
        ('Stewards', {
            'classes': ('collapse',),
            'fields': ('stewards_list', 'steward_inclusion_opt_in',),
        }),
        ('Remote', {
            'classes': ('collapse',),
            'fields': (
                'remote',
                'remote_locked',
                ('remote_site', 'remote_pk',),
            ),
        }),
        ('Geography', {
            'fields': (
                ('centroid', 'polygon'),
                ('polygon_area', 'polygon_width',),
            ),
        }),
    )


admin.site.unregister(Lot)
admin.site.register(Lot, LotAdmin)
