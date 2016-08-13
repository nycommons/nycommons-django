from livinglots_pathways.views import BasePathwaysDetailView, BasePathwaysListView

from .models import OrganizingPathway


class OrganizingPathwaysDetailView(BasePathwaysDetailView):
    model = OrganizingPathway


class OrganizingPathwaysListView(BasePathwaysListView):
    model = OrganizingPathway
