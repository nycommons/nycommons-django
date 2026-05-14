"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options

from livinglots import get_organizer_model
from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

register = template.Library()


class RenderOrganizerList(RenderGenericRelationList):
    model = get_organizer_model()
    template_dir_prefix = 'livinglots'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        KeywordArgument('public', default=False, required=False),
    )

    def get_context(self, context, target, public=False):
        context.update({
            self.get_model_plural_name(): self.get_objects(target, **public),
        })
        return context

    def get_objects(self, target, public=False):
        return self.model.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
            post_publicly=public,
        )

register.tag(RenderOrganizerList)


class GetOrganizerList(GetGenericRelationList):
    model = get_organizer_model()

register.tag(GetOrganizerList)


class GetOrganizerCount(GetGenericRelationCount):
    model = get_organizer_model()

register.tag(GetOrganizerCount)
