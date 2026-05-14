from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContentMixin(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, null=True, blank=True)
    added_by_name = models.CharField(_('added by name'), max_length=256,
                                     null=True, blank=True)

    class Meta:
        abstract = True
