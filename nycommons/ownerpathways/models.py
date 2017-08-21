from django.utils.translation import ugettext_lazy as _

from caching.base import CachingQuerySet, CachingMixin
from feincms.content.application import models as app_models
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin

from livinglots_pathways.models import BasePathway

from pathways.models import PathwayLotMixin, PathwayManager


class OwnerPathwayManager(PathwayManager):

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)


class OwnerPathway(PathwayLotMixin, CachingMixin, ContentModelMixin,
        BasePathway, Base):
    objects = OwnerPathwayManager()

    class Meta:
        verbose_name = _('Owner details')
        verbose_name_plural = _('Owner details')

    @app_models.permalink
    def get_absolute_url(self):
        return ('owner_pathway_detail', 'ownerpathways.urls', (), {
            'slug': self.slug,
        })


OwnerPathway.register_extensions(
    'feincms.module.extensions.translations',
)

OwnerPathway.register_regions(
    ('main', _('Main content area')),
)

OwnerPathway.create_content_type(RichTextContent)

OwnerPathway.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
