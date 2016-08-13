from livinglots_pathways.views import BasePathwaysDetailView, BasePathwaysListView

from .models import ReviewPathway


class ReviewPathwaysDetailView(BasePathwaysDetailView):
    model = ReviewPathway


class ReviewPathwaysListView(BasePathwaysListView):
    model = ReviewPathway
