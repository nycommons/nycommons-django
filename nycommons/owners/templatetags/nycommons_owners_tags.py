from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from django import template

from lots.models import Lot
from ..models import Owner


register = template.Library()


class GetOwnersByCommonsType(AsTag):
    options = Options(
        Argument('commons_type', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, commons_type):
        owner_pks = Lot.visible.filter(commons_type=commons_type) \
            .values_list('owner__pk', flat=True)
        owner_pks = list(set(owner_pks))
        return Owner.objects.filter(pk__in=owner_pks).distinct()


register.tag(GetOwnersByCommonsType)
