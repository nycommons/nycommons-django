from django.utils.translation import ugettext_lazy as _

from caching.base import CachingMixin
from feincms.content.application import models as app_models
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin

from livinglots_pathways.models import BasePathway

from pathways.models import PathwayLotMixin, PathwayManager


class OrganizingPathway(PathwayLotMixin, CachingMixin, ContentModelMixin,
        BasePathway, Base):
    objects = PathwayManager()

    class Meta:
        verbose_name = _('"How to Organize" pathway')

    @app_models.permalink
    def get_absolute_url(self):
        return ('organizing_pathway_detail', 'organizingpathways.urls', (), {
            'slug': self.slug,
        })


OrganizingPathway.register_extensions(
    'feincms.module.extensions.translations',
)

OrganizingPathway.register_regions(
    ('main', _('Main content area')),
)

OrganizingPathway.create_content_type(RichTextContent)

OrganizingPathway.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
