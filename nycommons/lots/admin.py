from django.contrib import admin
from django.forms import ModelForm

from dal import autocomplete
from livinglots_lots.admin import BaseLotAdmin

from .models import Lot


class LotAdminForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'owner': autocomplete.ModelSelect2(url='owners:owner-autocomplete')
        }


class LotAdmin(BaseLotAdmin):
    form = LotAdminForm
    list_display = ('address_line1', 'city', 'name', 'commons_type',)
    list_filter = ('commons_type', 'added', 'owner',)
    readonly_fields = ('added', 'group', 'stewards_list', 'updated',)
    fieldsets = (
        (None, {
            'fields': (
                ('bbl', 'name',),
                ('address_line1', 'address_line2', 'city', 'borough',),
                ('state_province', 'postal_code',),
                ('added', 'added_reason', 'updated',),
                ('owner', 'owner_opt_in'),
                'group',
                'is_waterfront',
            ),
        }),
        ('NYCHA filters', {
            'fields': (
                ('radpact_converted', 'radpact_planned',),
                (
                    'preservation_trust_voting_planned',
                    'preservation_trust_complete',
                ),
                (
                    'private_infill_planned',
                    'private_infill_completed',
                ),
                (
                    'section_8_pre_2014',
                ),
                (
                    'demolition_proposed',
                    'demolition_completed',
                ),
                (
                    'nycha_modernization_planned',
                    'nycha_modernization_complete',
                ),
                (
                    'new_public_housing_built',
                    'new_public_housing_planned',
                ),
            ),
        }),
        ('NYCHA Development Details', {
            'fields': (
                ('current_units', 'total_units', 'rental_rooms'),
                (
                    'population_section_8',
                    'population_public_housing',
                    'population_total',
                ),
                (
                    'families_fixed_income',
                    'families_fixed_income_percent',
                ),
                (
                    'buildings_residential',
                    'buildings_nonresidential',
                ),
                (
                    'buildings_stories',
                    'total_area',
                    'building_land_coverage',
                ),
                (
                    'cost_total',
                    'cost_per_room',
                    'rent_avg',
                ),
                ('senior_development', 'electricity_residents'),
                'private_management'
            ),
        }),
        ('RAD/PACT', {
            'fields': (
                'radpact_status',
                'radpact_conversion_date',
                ('radpact_developers', 'radpact_general_contractor',),
                ('radpact_property_manager', 'radpact_social_service_provider',),

            )
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
