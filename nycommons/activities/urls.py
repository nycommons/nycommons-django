from django.conf.urls import url

from .views import ActivityJSONListView


urlpatterns = [

    url(r'^list/json/', ActivityJSONListView.as_view(), name='activity_list'),

]


from actstream import urls as actstream_urls

urlpatterns += actstream_urls.urlpatterns


from inplace_activity_stream import urls as inplace_activity_stream_urls

urlpatterns += inplace_activity_stream_urls.urlpatterns
