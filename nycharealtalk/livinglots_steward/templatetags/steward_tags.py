from django import template

from livinglots import get_stewardproject_model
from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

register = template.Library()


class RenderStewardProjectList(RenderGenericRelationList):
    model = get_stewardproject_model()

register.tag(RenderStewardProjectList)


class GetStewardProjectList(GetGenericRelationList):
    model = get_stewardproject_model()

register.tag(GetStewardProjectList)


class GetStewardProjectCount(GetGenericRelationCount):
    model = get_stewardproject_model()

register.tag(GetStewardProjectCount)
