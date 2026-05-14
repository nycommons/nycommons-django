from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseGroundtruthRecord(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    actual_use = models.TextField(_('actual use'),
        help_text=_('How is this actually being used?'),
    )
    contact_name = models.CharField(_('contact name'),
        max_length=50,
        help_text=_("What's your name?"),
    )
    contact_email = models.EmailField(_('contact email'),
        blank=True,
        null=True,
        help_text=_('Who can we email for more information?'),
    )
    contact_phone = models.CharField(_('contact phone'),
        blank=True,
        null=True,
        max_length=20,
        help_text=_('Who can we call for more information?'),
    )
    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        editable=False,
        help_text=('When this record was added'),
    )

    class Meta:
        abstract = True
