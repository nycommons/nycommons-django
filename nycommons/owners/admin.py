from django.contrib import admin
from django.forms import ModelForm, SelectMultiple

from dal import autocomplete
from easy_select2 import apply_select2

from livinglots_owners.admin import (BaseOwnerAdmin, BaseOwnerContactAdmin,
                                     BaseOwnerGroupAdmin)

from .models import Owner, OwnerContact, OwnerGroup


class OwnerAdminForm(ModelForm):
    class Meta:
        # NB: setting fields = '__all__', less concerned about security since
        # we are in the admin site
        fields = '__all__'
        widgets = {
            'default_contact': autocomplete.ModelSelect2(url='owners:ownercontact-autocomplete'),
        }


class OwnerAdmin(BaseOwnerAdmin):
    form = OwnerAdminForm


class OwnerContactAdminForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'owner': autocomplete.ModelSelect2(url='owners:owner-autocomplete')
        }


class OwnerContactAdmin(BaseOwnerContactAdmin):
    form = OwnerContactAdminForm


class OwnerGroupAdminForm(ModelForm):
    class Meta:
        fields = ['name', 'owner_type', 'owners',]
        widgets = {
            'owners': apply_select2(SelectMultiple),
        }


class OwnerGroupAdmin(BaseOwnerGroupAdmin):
    form = OwnerGroupAdminForm


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
admin.site.register(OwnerGroup, OwnerGroupAdmin)
