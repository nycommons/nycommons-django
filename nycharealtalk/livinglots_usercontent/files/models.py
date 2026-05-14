from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..models import ContentMixin


class File(ContentMixin, models.Model):
    description = models.TextField(_('description'), null=True, blank=True)
    document = models.FileField(_('document'), upload_to='files')
    title = models.CharField(_('title'), max_length=256, null=True, blank=True)

    def __unicode__(self):
        if self.title:
            return self.title
        return u'%d' % self.pk
