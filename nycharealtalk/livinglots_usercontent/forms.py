from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class ContentForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        label='content type',
        queryset=ContentType.objects.all(),
        widget=forms.HiddenInput()
    )

    object_id = forms.IntegerField(
        label='object id',
        widget=forms.HiddenInput()
    )

    added_by = forms.ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    added_by_name = forms.CharField(
        label=_('Your name'),
        max_length=256,
        required=False,
        widget=forms.TextInput(),
    )

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.get('initial', {})

        # Add initial value for added_by based on the user kwarg
        try:
            user = kwargs['user']
            del kwargs['user']
            if not user.is_anonymous():
                kwargs['initial']['added_by'] = user
        except KeyError:
            pass

        super(ContentForm, self).__init__(*args, **kwargs)
