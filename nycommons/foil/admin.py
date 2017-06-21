# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import FoilContact


class FoilContactAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'officer_name',
        'officer_email',
        'appeal_officer_name',
        'appeal_officer_email',
    )

admin.site.register(FoilContact, FoilContactAdmin)
