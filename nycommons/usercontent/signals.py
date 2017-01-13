from django.db import models
from django.db.models.signals import class_prepared
from django.utils.translation import ugettext_lazy as _

def add_remote_fields(sender, **kwargs):

    if sender.__name__ not in ('File', 'Note',):
        return

    models.BooleanField(
        default=False,
        help_text=_('Is this from a remote site?'),
    ).contribute_to_class(sender, 'remote')

    models.CharField(
        blank=True,
        null=True,
        max_length=50,
        help_text=_('Which remote site is this from?'),
    ).contribute_to_class(sender, 'remote_site')

    models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_('What is the id of this on the remote site?'),
    ).contribute_to_class(sender, 'remote_pk')

    models.BooleanField(
        default=False,
        help_text=_('When refreshing from the remote site, can we update this one?'),
    ).contribute_to_class(sender, 'remote_locked')

class_prepared.connect(add_remote_fields);
