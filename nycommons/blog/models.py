from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
import feincms_cleanse

from elephantblog.models import Entry


class BlogArchiveContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('blog archive')
        verbose_name_plural = _('blog archive')

    def render(self, **kwargs):
        return render_to_string([
            'elephantblog/archive_plugin.html',
        ], {}, request=kwargs.get('request'))


class RecentPostsContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('recent posts')
        verbose_name_plural = _('recent posts')

    def render(self, **kwargs):
        # TODO get 10 most recent posts, pass in context
        return render_to_string([
            'elephantblog/recent_posts_plugin.html',
        ], {}, request=kwargs.get('request'))


Entry.register_extensions(
    'feincms.module.extensions.translations',
    'feincms.module.extensions.datepublisher',
)

Entry.register_regions(
    ('main', _('Main content area')),
    ('teaser', _('Blog entry teaser')),
)

Entry.create_content_type(
    RichTextContent,
    cleanse=feincms_cleanse.cleanse_html,
    regions=('main', 'teaser',)
)

Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
