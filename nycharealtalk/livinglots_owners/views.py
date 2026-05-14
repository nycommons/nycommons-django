from dal import autocomplete

from livinglots import get_owner_model, get_owner_contact_model


class OwnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return get_owner_model().objects.none()

        qs = get_owner_model().objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        owner_type = self.forwarded.get('owner_type', None)
        if owner_type:
            qs = qs.filter(owner_type=owner_type)

        qs.order_by('name')
        return qs


class OwnerContactAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return get_owner_contact_model().objects.none()

        qs = get_owner_contact_model().objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        qs.order_by('name')

        return qs
