from django.contrib import admin

from feincms.admin import item_editor

from livinglots_pathways.admin import BasePathwayAdmin

from .models import OwnerPathway


class OwnerPathwayAdmin(BasePathwayAdmin):
    fieldsets = [
        [None, {
            'fields': [
                ('is_active', 'author',),
                ('name', 'slug',),
            ],
        }],
        ['Which lots does this pathway apply to?', {
            'fields': [
                ('public_owners', 'specific_public_owners'),
                ('private_owners', 'specific_private_owners'),
                'only_waterfront_lots',
            ],
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]


admin.site.register(OwnerPathway, OwnerPathwayAdmin)
