# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import ModelForm

from dal import autocomplete, forward

from .models import FoilContact


class FoilContactAdminForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'owner': autocomplete.ModelSelect2(
                forward=(forward.Const('public', 'owner_type'),),
                url='owners:owner-autocomplete'
            )
        }


class FoilContactAdmin(admin.ModelAdmin):
    form = FoilContactAdminForm
    list_display = (
        'owner',
        'officer_name',
        'officer_email',
        'appeal_officer_name',
        'appeal_officer_email',
    )


admin.site.register(FoilContact, FoilContactAdmin)
