from livinglots_pathways.views import BasePathwaysDetailView, BasePathwaysListView

from .models import OwnerPathway


class OwnerPathwaysDetailView(BasePathwaysDetailView):
    model = OwnerPathway


class OwnerPathwaysListView(BasePathwaysListView):
    model = OwnerPathway
