# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Senator(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
    )
    email = models.EmailField(_('email'),
        blank=True,
        null=True,
    )
    url = models.URLField(_('url'),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name
