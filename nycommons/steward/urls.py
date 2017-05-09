from django.conf.urls import url

from .views import AddStewardNotificationView


urlpatterns = (

    url(r'^add/$', AddStewardNotificationView.as_view(),
        name='add_stewardnotification'),

)
