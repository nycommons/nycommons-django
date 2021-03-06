from django.conf.urls import url

from .views import OwnerPathwaysDetailView, OwnerPathwaysListView
                    

urlpatterns = [
    url(r'^$', OwnerPathwaysListView.as_view(), name='owner_pathway_list'),
    url(r'^(?P<slug>[^/]+)/$', OwnerPathwaysDetailView.as_view(),
        name='owner_pathway_detail'),
]
