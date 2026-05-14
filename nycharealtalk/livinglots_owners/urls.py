from django.conf.urls import url

from .views import OwnerAutocomplete, OwnerContactAutocomplete


urlpatterns = [
    url(
        r'^owner-autocomplete/$',
        OwnerAutocomplete.as_view(),
        name='owner-autocomplete'
    ),

    url(
        r'^ownercontact-autocomplete/$',
        OwnerContactAutocomplete.as_view(),
        name='ownercontact-autocomplete'
    )
]
