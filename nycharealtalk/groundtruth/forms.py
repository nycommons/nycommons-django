from django import forms

from livinglots_groundtruth.forms import GroundtruthRecordFormMixin

from .models import GroundtruthRecord


class GroundtruthRecordForm(GroundtruthRecordFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GroundtruthRecordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GroundtruthRecord
        fields = ('content_type', 'object_id', 'contact_name', 'contact_email',
                  'contact_phone', 'actual_use',)
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
