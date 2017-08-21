from django.db import models
from django.db.models import Q

from livinglots_pathways.models import BasePathwayManager

from lots.models import Lot


class PathwayManager(BasePathwayManager):

    def get_for_lot(self, lot):
        pathways = super(PathwayManager, self).get_for_lot(lot)

        # Waterfront lots
        if not lot.is_waterfront:
            pathways = pathways.exclude(only_waterfront_lots=True)

        return pathways


class PathwayLotMixin(models.Model):
    only_waterfront_lots = models.BooleanField(default=False)

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
        return Lot.objects.filter(filters)
    lots = property(get_lots)

    class Meta:
        abstract = True
