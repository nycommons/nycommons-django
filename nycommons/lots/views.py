from collections import OrderedDict
import geojson
import json
from operator import itemgetter
from pint import UnitRegistry
from random import shuffle
import re

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Sum
from django.views.generic import View

from caching.base import cached
from braces.views import JSONResponseMixin

from inplace.views import GeoJSONListView, PlacesDetailView
from livinglots_genericviews.views import JSONResponseView
from livinglots_lots.signals import lot_details_loaded
from livinglots_lots.views import FilteredLotsMixin, LotsCountView
from livinglots_lots.views import LotDetailView as BaseLotDetailView
from livinglots_lots.views import LotsCSV as BaseLotsCSV
from livinglots_lots.views import LotsKML as BaseLotsKML
from livinglots_lots.views import LotsGeoJSON as BaseLotsGeoJSON
from nycdata.parcels.models import Parcel
from organize.models import Organizer
from .models import Lot


ureg = UnitRegistry()


class LotDetailView(PlacesDetailView):
    model = Lot
    slug_field = 'bbl'
    slug_url_kwarg = 'bbl'

    def check_lot_sanity(self, request, lot):
        """
        Sanity check the lot. In particular, check for missing things every lot
        should have. Warn superusers if there is something amiss.
        """
        if not lot.centroid:
            messages.warning(request, ("This lot doesn't have a center point "
                                       "(centroid). You should edit the lot "
                                       "and add one."))
        if not lot.polygon:
            messages.warning(request, ("This lot doesn't have a shape "
                                       "(polygon). You should edit the lot "
                                       "and add one."))

    def get_object(self):
        lot = super(LotDetailView, self).get_object()
        if not (lot.is_visible or self.request.user.has_perm('lots.view_all_lots')):
            # Make an exception for lots with low known_use_certainty values,
            # which are being used in stealth mode right now
            if lot.known_use_certainty > 3:
                raise Http404
        return lot

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_superuser:
            self.check_lot_sanity(request, self.object)

        # Redirect to the lot's group, if it has one
        lot_details_loaded.send(sender=self, instance=self.object)
        if self.object.group:
            messages.info(request, _("The lot you requested is part of a "
                                     "group. Here is the group's page."))
            return HttpResponseRedirect(self.object.group.get_absolute_url())
        return super(LotDetailView, self).get(request, *args, **kwargs)


class LotDetailViewJSON(JSONResponseMixin, BaseLotDetailView):
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def round_acres(self, lot):
        try:
            # Attempt to round to smallest number of digits we can
            decimal_places = 1
            rounded = 0
            area_acres = lot.area_acres
            if not area_acres:
                return None
            while not rounded:
                rounded = round(area_acres, decimal_places)
                decimal_places += 1
            return rounded
        except TypeError:
            return None

    def get(self, request, *args, **kwargs):
        lot = self.object = self.get_object()

        context = {
            'area_acres': self.round_acres(lot),
            'bbl': lot.bbl,
            'centroid': {
                'x': lot.centroid.x,
                'y': lot.centroid.y,
            },
            'name': lot.display_name,
            'number_of_lots': lot.number_of_lots,
            'part_of_group': lot.group is not None,
            'url': lot.get_absolute_url(),
        }
        if lot.owner:
            context['owner'] = lot.owner.name

        return self.render_json_response(context)


class LotGeoJSONMixin(object):

    def get_acres(self, lot):
        acres = getattr(lot, 'area_acres', None)
        if not acres:
            return 'unknown'
        return round(acres, 2)

    def get_layer(self, lot):
        if lot.known_use:
            return 'in_use'
        elif lot.owner and lot.owner.owner_type == 'public':
            return 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            return 'private'
        return ''

    def get_properties(self, lot):
        return {
            'address_line1': lot.address_line1,
            'has_organizers': lot.organizers__count > 0,
            'layer': self.get_layer(lot),
            'number_of_lots': lot.number_of_lots,
            'number_of_lots_plural': lot.number_of_lots > 1,
            'owner': str(lot.owner) or 'unknown',
            'pk': lot.pk,
            'size': self.get_acres(lot),
        }

    def get_geometry(self, lot):
        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return json.loads(lot_geojson)

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=self.get_geometry(lot),
            properties=self.get_properties(lot),
        )


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type'
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            features = super(LotsGeoJSONCentroid, self).get_features()
            shuffle(features)
            return features
        return cached(_get_value, key, 60 * 15)


class LotsGeoJSONPolygon(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_properties(self, lot):
        properties = super(LotsGeoJSONPolygon, self).get_properties(lot)
        properties['centroid'] = (
            round(lot.centroid.x, 4),
            round(lot.centroid.y, 4)
        )
        return properties

    def get_queryset(self):
        return self.get_lots().qs.filter(polygon__isnull=False).geojson(
            field_name='polygon',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type'
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            return super(LotsGeoJSONPolygon, self).get_features()
        return cached(_get_value, key, 60 * 15)


class LotsOwnershipOverview(FilteredLotsMixin, JSONResponseView):

    layer_labels = {
        'community_project': 'community project',
        'priority': 'priority',
        'library': 'library',
        'public_housing': 'public housing site',
        'post_office': 'post office',
    }

    def count_organizers(self, lots_qs):
        return Organizer.objects.filter(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id__in=lots_qs.values_list('pk', flat=True)
        ).count()

    def get_owners(self, lots_qs):
        owners = []
        for row in lots_qs.values('owner__name').annotate(count=Count('pk'), area=Sum('polygon_area')).order_by():
            try:
                area = float(row['area'])
            except TypeError:
                area = None
            owners.append({
                'name': row['owner__name'],
                'area': area,
                'count': row['count'],
            })
        return sorted(owners, key=itemgetter('name'))

    def get_layers(self, lots):
        return OrderedDict([
            ('community_project', lots.filter(steward_projects__isnull=False)),
            ('priority', lots.filter(priority=True)),
            ('library', lots.filter(commons_type='library')),
            ('public_housing', lots.filter(commons_type='public housing')),
            ('post_office', lots.filter(commons_type='post office')),
        ])

    def get_layer_counts(self, layers):
        counts = []
        for layer, qs in layers.items():
            owners = self.get_owners(qs)
            if owners:
                counts.append({
                    'count': sum([o['count'] for o in owners]),
                    'label': self.layer_labels[layer],
                    'organizers_count': self.count_organizers(qs),
                    'owners': owners,
                    'priority': layer in ('community_project', 'priority',),
                    'type': layer,
                })
        return counts

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        layers = self.get_layers(lots)
        return self.get_layer_counts(layers)


class LotsCountViewWithAcres(LotsCountView):

    def get_area_in_acres(self, lots_qs):
        sqft = lots_qs.aggregate(total_area=Sum('polygon_area'))['total_area']
        if not sqft:
            return 0
        sqft = sqft * (ureg.feet ** 2)
        acres = sqft.to(ureg.acre).magnitude
        return int(round(acres))

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        no_known_use = lots.filter(known_use__isnull=True)
        in_use = lots.filter(known_use__isnull=False, known_use__visible=True)

        context = {
            'lots-count': lots.count(),
            'lots-acres': self.get_area_in_acres(lots),
            'no-known-use-count': no_known_use.count(),
            'no-known-use-acres': self.get_area_in_acres(no_known_use),
            'in-use-count': in_use.count(),
            'in-use-acres': self.get_area_in_acres(in_use),
        }
        return context


class LotsCSV(BaseLotsCSV):

    def get_sitename(self):
        # TODO replace with site name
        return ''


class LotsKML(BaseLotsKML):

    def get_sitename(self):
        # TODO replace with site name
        return ''


class LotsGeoJSON(BaseLotsGeoJSON):

    def get_sitename(self):
        # TODO replace with site name
        return ''


class SearchView(JSONResponseMixin, View):
    # BBL is ten digits
    bbl_pattern = re.compile(r'.*(\d{10}).*')

    # Look for something of the form <borough> <block> <lot>, no matter what is
    # separating each
    borough_block_lot_pattern = re.compile(r'.*?(\w+)\D+(\d+)\D+(\d+).*?')

    def get_search_results(self, q, max=5):
        return (self.get_lot_results(q, max=max) +
                self.get_parcel_results(q, max=max))[:max]

    def get_lot_results(self, q, max=5):
        def _lot_result_dict(lot):
            return {
                'longitude': lot.centroid.x,
                'latitude': lot.centroid.y,
                'name': lot.name,
            }
        return [_lot_result_dict(l) for l in Lot.objects.filter(name__icontains=q)[:max]]

    def get_parcel_results(self, q, max=5):
        def _parcel_result_dict(parcel):
            return {
                'longitude': parcel.geom.centroid.x,
                'latitude': parcel.geom.centroid.y,
                'name': parcel.bbl,
            }

        # Try to get a bbl we can search by
        try:
            bbl = self.bbl_pattern.match(q).group(1)
        except Exception:
            try:
                # Try to find borough, block, and lot, convert to bbl
                bbl = build_bbl(*self.borough_block_lot_pattern.match(q).groups())
            except Exception:
                bbl = None

        if bbl:
            return [_parcel_result_dict(p) for p in Parcel.objects.filter(bbl=bbl)[:max]]
        return []

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'results': self.get_search_results(request.GET.get('q', None)),
        })
