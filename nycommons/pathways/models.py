from django.db import models
from django.db.models import Q

from lots.models import Lot


class PathwayLotMixin(models.Model):

    def get_lots(self):
        """Get the lots this pathway applies to"""
        filters = Q()
        if self.private_owners:
            if self.specific_private_owners.exists():
                print self.specific_private_owners.all().values_list('pk', flat=True)
                filters |= Q(
                    owner__owner_type='private',
                    owner__pk__in=self.specific_private_owners.all().values_list('pk',
                        flat=True),
                )
            else:
                filters |= Q(owner__owner_type='private')
        if self.public_owners:
            if self.specific_public_owners.exists():
                print self.specific_public_owners.all().values_list('pk', flat=True)
                filters |= Q(
                    owner__owner_type='public',
                    owner__pk__in=self.specific_public_owners.all().values_list('pk',
                        flat=True),
                )
            else:
                filters |= Q(owner__owner_type='public')
        return Lot.objects.filter(filters)
    lots = property(get_lots)

    class Meta:
        abstract = True
