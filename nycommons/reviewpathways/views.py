from django.views.generic.list import ListView

from livinglots_pathways.views import BasePathwaysDetailView

from .models import ReviewPathway


class ReviewPathwaysDetailView(BasePathwaysDetailView):
    model = ReviewPathway


class ReviewPathwaysListView(ListView):
    model = ReviewPathway
