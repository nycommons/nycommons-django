from django.conf.urls import patterns, url

from .views import OrganizingPathwaysDetailView, OrganizingPathwaysListView
                    


urlpatterns = patterns('',
    url(r'^$', OrganizingPathwaysListView.as_view(),
        name='organizing_pathway_list'),
    url(r'^(?P<slug>[^/]+)/$', OrganizingPathwaysDetailView.as_view(),
        name='organizing_pathway_detail'),
)
