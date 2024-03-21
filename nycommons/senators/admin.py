# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from inplace.boundaries.models import Boundary

from .models import Senator


class SenatorForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Senator


class SenatorAdmin(admin.ModelAdmin):
    form = SenatorForm
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Senator, SenatorAdmin)
