from django import template
from django.core.cache import cache

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from livinglots import get_lot_model, get_owner_model, get_owner_group_model

register = template.Library()


class GetOwners(AsTag):
    options = Options(
        'type',
        Argument('owner_type', required=True, resolve=True),
        Argument('grouped', required=False, resolve=True),
        Argument('visible_only', required=False, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def fetch_owners(self, owner_type, grouped=False, visible_only=True):
        """Get owners from database"""
        owners = get_owner_model().objects.filter(
            owner_type=owner_type
        ).order_by('name')

        if visible_only:
            owners = [o for o in owners if get_lot_model().visible.filter(owner=o).exists()]

        if grouped:
            # Get all ownergroups for type
            groups = get_owner_group_model().objects.filter(owner_type=owner_type)

            # Remove owners in groups
            grouped_owners = groups.values_list('owners', flat=True)
            owners = [o for o in owners if o.pk not in grouped_owners]

            # Insert into owners and sort again
            owners += groups
            owners = sorted(owners, key=lambda o: o.name)
        return owners

    def get_owners(self, owner_type, grouped=False, visible_only=True):
        """Get owners from cache or fetch from database and store in cache"""
        cache_key = 'owner_tags:get_owners:%s:%s:%s' % (
            owner_type,
            str(grouped),
            str(visible_only),
        )
        owners = cache.get(cache_key)
        if not owners:
            owners = self.fetch_owners(owner_type, grouped=grouped,
                                       visible_only=visible_only)
            cache.set(cache_key, owners, 30 * 60)
        return owners

    def get_value(self, context, owner_type, grouped, visible_only):
        return self.get_owners(owner_type, grouped=grouped,
                               visible_only=visible_only)


register.tag(GetOwners)
