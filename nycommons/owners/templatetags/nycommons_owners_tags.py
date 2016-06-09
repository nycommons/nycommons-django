from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from django import template

from ..models import Owner


register = template.Library()


class GetOwnersByCommonsType(AsTag):
    options = Options(
        Argument('commons_type', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, commons_type):
        return Owner.objects.filter(lot__commons_type=commons_type).distinct()


register.tag(GetOwnersByCommonsType)
