from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from ..models import ReviewPathway

register = template.Library()


class ReviewPathwaysTag(object):

    def get_objects(self, target):
        return ReviewPathway.objects.get_for_lot(target)


class RenderReviewPathwaySummaryList(ReviewPathwaysTag, InclusionTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True)
    )
    template = 'reviewpathways/reviewpathway_summary_list.html'

    def get_context(self, context, target):
        context.update({
            'pathways': self.get_objects(target),
        })
        return context

register.tag(RenderReviewPathwaySummaryList)


class GetReviewPathways(ReviewPathwaysTag, AsTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        return self.get_objects(target)

register.tag(GetReviewPathways)
