"""
Template tags for the usercontent

"""
import itertools

from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag

from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList)

from ..files.models import File
from ..notes.models import Note
from ..photos.models import Photo

register = template.Library()


class AdminActions(InclusionTag):
    options = Options(
        Argument('usercontent', required=True, resolve=True)
    )
    template = 'livinglots/usercontent/admin_actions.html'

    def get_context(self, context, usercontent, **kwargs):
        app_name = usercontent._meta.app_label
        model_name = usercontent._meta.object_name.lower()
        context.update({
            'app_name': app_name,
            'change_perm': '%s.change_%s' % (app_name, model_name,),
            'change_url_name': 'admin:%s_%s_change' % (app_name, model_name,),
            'delete_perm': '%s.delete_%s' % (app_name, model_name,),
            'delete_url_name': 'admin:%s_%s_delete' % (app_name, model_name,),
            'model_name': model_name,
            'obj': usercontent,
        })
        return context


class AllUserContentMixin(object):
    models = (File, Note, Photo,)

    def get_objects(self, target):
        """Pull instances from each model and combine"""
        kwargs = {
            'content_type': ContentType.objects.get_for_model(target),
            'object_id': target.pk,
        }
        content = [model.objects.filter(**kwargs) for model in self.models]
        content = list(itertools.chain.from_iterable(content))
        return sorted(content, key=lambda c: c.added, reverse=True)


class GetUserContentList(AllUserContentMixin, GetGenericRelationList):
    pass


class RenderUserContent(InclusionTag):
    options = Options(
        Argument('usercontent', required=True, resolve=True)
    )
    template = ''

    def get_context(self, context, usercontent, **kwargs):
        context.update({
            'app_name': usercontent._meta.app_label,
            'model_name': usercontent._meta.object_name.lower(),
            'obj': usercontent,
            usercontent._meta.object_name.lower(): usercontent,
        })
        return context

    def get_template(self, context, usercontent, **kwargs):
        return 'livinglots/usercontent/%s.html' % (
            usercontent._meta.object_name.lower(),
        )


class RenderUserContentList(AllUserContentMixin, RenderGenericRelationList):

    def get_template(self, context, **kwargs):
        return 'livinglots/usercontent/list.html'

    def get_model_plural_name(self):
        return 'usercontent'


register.tag(AdminActions)
register.tag(GetUserContentList)
register.tag(RenderUserContent)
register.tag(RenderUserContentList)
