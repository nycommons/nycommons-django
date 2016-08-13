from django.conf.urls import patterns, url

from .views import ReviewPathwaysDetailView, ReviewPathwaysListView


urlpatterns = patterns('',
    url(r'^$', ReviewPathwaysListView.as_view(), name='review_pathway_list'),
    url(r'^list/$', ReviewPathwaysListView.as_view(), name='review_pathway_list'),

    url(r'^(?P<slug>[^/]+)/$', ReviewPathwaysDetailView.as_view(),
        name='review_pathway_detail'),
)
