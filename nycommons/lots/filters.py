from hashlib import sha1
import json

from django.db.models import Q

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D

import django_filters
from inplace.boundaries.models import Boundary

from .models import Lot, COMMONS_TYPES


class BoundaryFilter(django_filters.Filter):

    def filter(self, qs, value):
        name, pk = value.split('::')
        try:
            return qs.filter(
                centroid__within=Boundary.objects.get(layer__name=name, pk=pk).geometry
            )
        except Boundary.DoesNotExist:
            print 'Could not find Boundary %s %s' % (name, pk)
        return qs


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class LotGroupParentFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(group=None)
        return qs


class LotCenterFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        try:
            lot = Lot.objects.get(pk=value)
        except Exception:
            return qs
        return qs.filter(centroid__distance_lte=(lot.centroid, D(mi=.5)))


class OrganizingFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(organizing=True)
        return qs


class OwnerFilter(django_filters.Filter):

    def __init__(self, owner_type=None, **kwargs):
        super(OwnerFilter, self).__init__(**kwargs)
        self.owner_type = owner_type

    def filter(self, qs, value):
        if not value:
            return qs
        owner_pks = value.split(',')
        owner_query = Q(
            Q(known_use=None) | Q(known_use__visible=True),
            owner__owner_type=self.owner_type,
            owner__pk__in=owner_pks,
        )
        other_owners_query = ~Q(owner__owner_type=self.owner_type)
        return qs.filter(owner_query | other_owners_query)


class OwnersFilter(django_filters.Filter):

    def filter(self, qs, value):
        try:
            owners_query = Q()
            for commons_type, owner_pks in json.loads(value).items():
                owners_query |= Q(
                    commons_type=commons_type,
                    owner__pk__in=owner_pks,
                )
            return qs.filter(owners_query)
        except ValueError:
            return qs


class PriorityFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(priority=True)
        return qs


class PriorityOrganizingFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(organizing=True, priority=True)
        return qs


class ProjectFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value or value == 'include':
            return qs
        has_project_filter = Q(known_use__visible=True)
        if value == 'include':
            return qs
        elif value == 'exclude':
            return qs.filter(~has_project_filter)
        elif value == 'only':
            return qs.filter(has_project_filter)
        return qs


class LotFilter(django_filters.FilterSet):
    bbox = BoundingBoxFilter()
    boundary = BoundaryFilter()
    commons_type = django_filters.MultipleChoiceFilter(
        choices=COMMONS_TYPES,
        widget=django_filters.widgets.CSVWidget()
    )
    lot_center = LotCenterFilter()
    organizing = OrganizingFilter()
    owners = OwnersFilter()
    parents_only = LotGroupParentFilter()
    priority = PriorityFilter()
    priority_organizing = PriorityOrganizingFilter()
    projects = ProjectFilter()
    public_owners = OwnerFilter(owner_type='public')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        self.user = user

    def hashkey(self):
        return sha1(repr(sorted(self.data.items()))).hexdigest()

    class Meta:
        model = Lot
        fields = [
            'address_line1',
            'bbox',
            'boundary',
            'commons_type',
            'known_use',
            'lot_center',
            'organizing',
            'owners',
            'parents_only',
            'priority',
            'priority_organizing',
            'projects',
            'public_owners',
        ]
