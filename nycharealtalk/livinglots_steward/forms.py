from django import forms


class StewardNotificationFormMixin(forms.ModelForm):

    class Meta:
        fields = (
            # Hidden fields
            'content_type', 'object_id',

            # Organizer fields
            'name', 'phone', 'email', 'type', 'url', 'facebook_page',

            # StewardProject fields
            'project_name', 'use', 'land_tenure_status',
            'support_organization', 'include_on_map',
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
