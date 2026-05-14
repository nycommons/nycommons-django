from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from actstream.models import Action

register = template.Library()


class ActivityTagMixin(object):

    def get_activities(self, count):
        return Action.objects.all().order_by('-timestamp')[:count]


class GetActivities(ActivityTagMixin, AsTag):
    options = Options(
        Argument('count', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, count):
        return self.get_activities(count)

register.tag(GetActivities)
