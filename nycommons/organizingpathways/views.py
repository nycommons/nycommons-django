from django.views.generic.list import ListView

from livinglots_pathways.views import BasePathwaysDetailView

from .models import OrganizingPathway


class OrganizingPathwaysDetailView(BasePathwaysDetailView):
    model = OrganizingPathway


class OrganizingPathwaysListView(ListView):
    model = OrganizingPathway
