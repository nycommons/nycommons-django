from django.conf.urls import url

from livinglots import get_organizer_model

from .views import (AddParticipantSuccessView, DeleteOrganizerView,
                    DeleteWatcherView, EditLotParicipantView,
                    NotificationPreview)


urlpatterns = [

    url(r'^(?P<object_pk>\d+)/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=get_organizer_model(),
        ),
        name='add_organizer_success'),

    url(r'^organize/(?P<hash>[^/]{30,})/edit/$',
        EditLotParicipantView.as_view(),
        name='edit_participant'),

    url(r'^organizers/(?P<hash>[^/]{30,})/delete/(?P<organizer_pk>\d+)/$',
        DeleteOrganizerView.as_view(),
        name='delete_organizer'),

    url(r'^watchers/(?P<hash>[^/]{30,})/delete/(?P<watcher_pk>\d+)/$',
        DeleteWatcherView.as_view(),
        name='delete_watcher'),

    url(r'^organize/notifications/(?P<slug>\S+)/preview/$',
        NotificationPreview.as_view(),
        name='notification_preview'),

]
