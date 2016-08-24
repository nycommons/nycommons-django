from django.db import models
from django.utils.translation import ugettext_lazy as _


class RemoteMixin(models.Model):
    """
    A mixin adding data to track remote entities--entities that are largely
    hosted on another site but are mirrored here.
    """
    remote = models.BooleanField(
        default=False,
        help_text=_('Is this from a remote site?'),
    )
    remote_site = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        help_text=_('Which remote site is this from?'),
    )
    remote_pk = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_('What is the id of this on the remote site?'),
    )
    remote_locked = models.BooleanField(
        default=False,
        help_text=_('When refreshing from the remote site, can we update this one?'),
    )

    class Meta:
        abstract = True
