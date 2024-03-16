from django.db import models
from django.db.models import Q

from caching.base import CachingQuerySet

from livinglots_pathways.models import BasePathwayManager

from lots.models import Lot


class PathwayManager(BasePathwayManager):

    def get_for_lot(self, lot):
        pathways = super(PathwayManager, self).get_for_lot(lot)

        # Waterfront lots
        if not lot.is_waterfront:
            pathways = pathways.exclude(only_waterfront_lots=True)

        # Landmarked lots
        if not len(lot.landmarks) > 0:
            pathways = pathways.exclude(only_landmarked_lots=True)

        # Urban renewal lots
        if not len(lot.urban_renewal_records) > 0:
            pathways = pathways.exclude(only_urban_renewal_lots=True)

        # TODO NYCHA

        return pathways

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)


class PathwayLotMixin(models.Model):
    only_waterfront_lots = models.BooleanField(default=False)
    only_landmarked_lots = models.BooleanField(default=False)
    only_urban_renewal_lots = models.BooleanField(default=False)

    # nycha filters
    radpact_converted = models.BooleanField(
        default=False,
        verbose_name='RAD/PACT - Converted to Section 8 Under Private Management'
    )
    radpact_planned = models.BooleanField(
        default=False,
        verbose_name='Planned RAD/PACT - Section 8 Conversion Under Private Management'
    )
    preservation_trust_voting_planned = models.BooleanField(
        default=False,
        verbose_name='Voting Planned for Preservation Trust Section 8 Conversion'
    )
    preservation_trust_complete = models.BooleanField(
        default=False,
        verbose_name='Preservation Trust Conversion Complete'
    )
    private_infill_planned = models.BooleanField(
        default=False,
        verbose_name='Private Infill Planned'
    )
    section_8_pre_2014 = models.BooleanField(
        default=False,
        verbose_name='Conversions to Section 8 Completed Prior to 2014'
    )
    demolition_proposed = models.BooleanField(
        default=False,
        verbose_name='Demolition Proposed',
    )
    demolition_completed = models.BooleanField(
        default=False,
        verbose_name='Demolition Completed',
    )
    nycha_modernization_planned = models.BooleanField(
        default=False,
        verbose_name='NYCHA-managed Modernization Planned'
    )
    nycha_modernization_complete = models.BooleanField(
        default=False,
        verbose_name='NYCHA Completed Modernization'
    )
    new_public_housing_built = models.BooleanField(
        default=False,
        verbose_name='New Public Housing Built Since 1998'
    )
    new_public_housing_planned = models.BooleanField(
        default=False,
        verbose_name='New Public Housing Planned Since 1998'
    )

    def get_lots(self):
        """Get the lots this pathway applies to"""
        filters = Q()
        owner_filters = Q()
        if self.private_owners:
            if self.specific_private_owners.exists():
                owner_filters |= Q(
                    owner__owner_type='private',
                    owner__pk__in=self.specific_private_owners.all().values_list('pk',
                        flat=True),
                )
            else:
                owner_filters |= Q(owner__owner_type='private')
        if self.public_owners:
            if self.specific_public_owners.exists():
                owner_filters |= Q(
                    owner__owner_type='public',
                    owner__pk__in=self.specific_public_owners.all().values_list('pk',
                        flat=True),
                )
            else:
                owner_filters |= Q(owner__owner_type='public')
        filters &= owner_filters
        if self.only_waterfront_lots:
            filters &= Q(is_waterfront=True)
        if self.only_landmarked_lots:
            filters &= Q(parcel__landmark_object__isnull=False)
        if self.only_urban_renewal_lots:
            filters &= Q(parcel__urbanrenewalrecord__isnull=False)

        # TODO add nycha filters
        return Lot.objects.filter(filters)
    lots = property(get_lots)

    class Meta:
        abstract = True
