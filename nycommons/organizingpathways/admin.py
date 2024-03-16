from django.contrib import admin

from feincms.admin import item_editor

from livinglots_pathways.admin import BasePathwayAdmin

from pathways.admin import PathwayAdminForm
from .models import OrganizingPathway


class OrganizingPathwayAdmin(BasePathwayAdmin):
    form = PathwayAdminForm
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
                'only_landmarked_lots',
                'only_urban_renewal_lots',
                'radpact_converted',
                'radpact_planned',
                'preservation_trust_voting_planned',
                'preservation_trust_complete',
                'private_infill_planned',
                'section_8_pre_2014',
                'demolition_proposed',
                'demolition_completed',
                'nycha_modernization_planned',
                'nycha_modernization_complete',
                'new_public_housing_built',
                'new_public_housing_planned',
            ],
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]


admin.site.register(OrganizingPathway, OrganizingPathwayAdmin)
