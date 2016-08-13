from django.utils.translation import ugettext_lazy as _

from caching.base import CachingQuerySet, CachingMixin
from feincms.content.application import models as app_models
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin

from livinglots_pathways.models import BasePathway, BasePathwayManager


class ReviewPathwayManager(BasePathwayManager):

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)


class ReviewPathway(CachingMixin, ContentModelMixin, BasePathway, Base):
    objects = ReviewPathwayManager()

    @app_models.permalink
    def get_absolute_url(self):
        return ('review_pathway_detail', 'reviewpathways.urls', (), {
            'slug': self.slug,
        })


ReviewPathway.register_extensions(
    'feincms.module.extensions.translations',
)

ReviewPathway.register_regions(
    ('main', _('Main content area')),
)

ReviewPathway.create_content_type(RichTextContent)

ReviewPathway.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
