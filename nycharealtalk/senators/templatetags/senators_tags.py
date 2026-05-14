from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from ..models import Senator

register = template.Library()


class Senators(AsTag):
    options = Options(
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context):
        try:
            return Senator.objects.all()
        except IndexError:
            return None


register.tag(Senators)
