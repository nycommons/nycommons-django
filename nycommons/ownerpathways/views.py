from django.views.generic.list import ListView

from livinglots_pathways.views import BasePathwaysDetailView

from .models import OwnerPathway


class OwnerPathwaysDetailView(BasePathwaysDetailView):
    model = OwnerPathway


class OwnerPathwaysListView(ListView):
    model = OwnerPathway
