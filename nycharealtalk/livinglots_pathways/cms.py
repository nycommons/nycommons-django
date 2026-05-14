from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.content.application import models as app_models
from feincms.module.mixins import ContentModelMixin

from livinglots import get_pathway_model


class PathwayFeinCMSMixin(ContentModelMixin):

    @app_models.permalink
    def get_absolute_url(self):
        return ('pathway_detail', 'pathways.urls', (), {
            'slug': self.slug,
        })


class PathwayListContent(models.Model):

    def render(self, **kwargs):
        ctx = {
            'pathways': get_pathway_model().objects.all().order_by('name'),
        }
        ctx.update(kwargs)
        return render_to_string([
            'pathways/pathway_list_content.html',
        ], ctx, context_instance=kwargs.get('context'))

    class Meta:
        abstract = True
        verbose_name = _('Pathway list')
        verbose_name_plural = _('Pathway list')
