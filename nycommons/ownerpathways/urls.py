from django.conf.urls import patterns, url

from .views import OwnerPathwaysDetailView, OwnerPathwaysListView
                    

urlpatterns = patterns('',
    url(r'^$', OwnerPathwaysListView.as_view(), name='owner_pathway_list'),
    url(r'^(?P<slug>[^/]+)/$', OwnerPathwaysDetailView.as_view(),
        name='owner_pathway_detail'),
)
