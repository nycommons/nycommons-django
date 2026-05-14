from django.conf.urls import patterns, url

from .views import Preview


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/preview/$', Preview.as_view(), name='mailings_preview'),
)
