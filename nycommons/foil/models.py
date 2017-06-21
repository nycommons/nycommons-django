# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from owners.models import Owner


class FoilContact(models.Model):
    owner = models.ForeignKey(Owner,
        help_text=_('The owner (agency) this contact applies to')
    )

    officer_name = models.CharField(
        max_length=300,
        help_text=_('The name of the FOIL officer'),
        blank=True,
        null=True
    )
    officer_email = models.EmailField(
        help_text=_('The email of the FOIL officer'),
        blank=True,
        null=True
    )

    appeal_officer_name = models.CharField(
        max_length=300,
        help_text=_('The name of the FOIL appeal officer'),
        blank=True,
        null=True
    )
    appeal_officer_email = models.EmailField(
        help_text=_('The email of the FOIL appeal officer'),
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __unicode__(self):
        try:
            return '%s' % self.owner.name
        except Exception:
            return u'%d' % self.pk
