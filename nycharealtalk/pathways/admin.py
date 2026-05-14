from django.forms import ModelForm

from dal import autocomplete, forward


class PathwayAdminForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'specific_private_owners': autocomplete.ModelSelect2Multiple(
                forward=(forward.Const('private', 'owner_type'),),
                url='owners:owner-autocomplete'
            ),
            'specific_public_owners': autocomplete.ModelSelect2Multiple(
                forward=(forward.Const('public', 'owner_type'),),
                url='owners:owner-autocomplete'
            ),
        }
