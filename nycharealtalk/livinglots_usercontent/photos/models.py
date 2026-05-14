from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import Transpose
from imagekit.processors.resize import SmartResize

from ..models import ContentMixin


class Photo(ContentMixin, models.Model):
    original_image = models.ImageField(_('original image'), upload_to='photos')
    formatted_image = ImageSpecField(
        format='JPEG',
        options={'quality': 90},
        processors=[Transpose(),],
        source='original_image',
    )
    thumbnail = ImageSpecField(
        processors=[SmartResize(200, 200), Transpose(),],
        format='JPEG',
        options={'quality': 90},
        source='original_image',
    )

    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)

    def __unicode__(self):
        if self.name:
            return self.name
        return u'%d' % self.pk
