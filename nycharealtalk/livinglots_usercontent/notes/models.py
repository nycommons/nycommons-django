from HTMLParser import HTMLParser

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..models import ContentMixin


class Note(ContentMixin, models.Model):
    text = models.TextField(_('text'))
    
    def _text_unescaped(self):
        return HTMLParser().unescape(self.text)

    text_unescaped = property(_text_unescaped)

    def __unicode__(self):
        return '%d' % self.pk
