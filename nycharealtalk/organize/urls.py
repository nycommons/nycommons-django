from django.conf.urls import url

import livinglots_organize.urls as llurls

from .views import AddOrganizerView, SubscribeView


urlpatterns = llurls.urlpatterns + [

    url(r'^add/organizer/', AddOrganizerView.as_view(), name='add_organizer'),
    url(r'^subscribe/', SubscribeView.as_view(), name='subscribe'),

]
