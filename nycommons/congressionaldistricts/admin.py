# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from inplace.boundaries.models import Boundary

from .models import CongressMember


class CongressMemberForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=Boundary.objects.filter(
            layer__name='congressional districts',
        ),
    )

    class Meta:
        fields = '__all__'
        model = CongressMember


class CongressMemberAdmin(admin.ModelAdmin):
    form = CongressMemberForm
    list_display = ('name', 'district',)
    search_fields = ('name',)


admin.site.register(CongressMember, CongressMemberAdmin)
