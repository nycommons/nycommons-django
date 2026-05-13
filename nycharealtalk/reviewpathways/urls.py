from django.conf.urls import url

from .views import ReviewPathwaysDetailView, ReviewPathwaysListView


urlpatterns = [
    url(r'^$', ReviewPathwaysListView.as_view(), name='review_pathway_list'),
    url(r'^(?P<slug>[^/]+)/$', ReviewPathwaysDetailView.as_view(),
        name='review_pathway_detail'),
]
