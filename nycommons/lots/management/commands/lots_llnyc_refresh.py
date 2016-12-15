import geojson
import requests

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from lots.models import Lot
from owners.models import Owner


class Command(BaseCommand):
    help = 'Refresh data from LLNYC'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.count = 0
        self.create_count = 0
        self.delete_count = 0
        self.update_count = 0

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            default=False,
            help='Perform a dry-run',
        )

    def load_lots(self, verbosity=1, **kwargs):
        lots_geojson = self.get_geojson(verbosity=verbosity)
        for feature in lots_geojson.features:
            self.count += 1
            self.load_lot_from_feature(feature, verbosity=verbosity, **kwargs)
        self.delete_missing_lots(lots_geojson.features, verbosity=verbosity,
                **kwargs)

        if verbosity > 0:
            self.print_report()

    def print_report(self):
        self.stdout.write('\nDone! Loaded %d lots' % self.count)
        self.stdout.write('-------------------------------')
        self.stdout.write('Created: %d' % self.create_count)
        self.stdout.write('Deleted: %d' % self.delete_count)
        self.stdout.write('Updated: %d' % self.update_count)

    def get_geojson(self, verbosity=1):
        url = settings.REMOTE_LOTS['llnyc']['api_lots_url']
        request = requests.get(url)
        if verbosity >= 2:
            self.stdout.write('Loaded %s with status code %d' % (
                url, request.status_code
            ))
        return geojson.loads(request.text)

    def load_lot_from_feature(self, feature, verbosity=1, **kwargs):
        """Load / update a lot from a geojson feature."""
        if verbosity >= 3:
            self.stdout.write(str(feature['properties']))
        lot = self.get_lot(feature)
        if lot:
            if not lot.remote_locked:
                lot = self.update_lot(lot, feature, **kwargs)
        else:
            lot = self.create_lot(feature, **kwargs)
        return lot

    def get_lot(self, feature):
        try:
            return Lot.objects.get(
                remote=True,
                remote_site='llnyc',
                remote_pk=feature['properties']['pk'],
            )
        except Lot.DoesNotExist:
            return None

    def update_lot(self, lot, feature, dry_run=False):
        self.update_count += 1
        kwargs = self.lot_kwargs(feature)
        kwargs['polygon'] = GEOSGeometry(str(feature['geometry']))
        if dry_run:
            self.stdout.write('Update lot %d' % lot.pk)
        else:
            Lot.objects.filter(pk=lot.pk).update(**kwargs)
        return lot

    def create_lot(self, feature, dry_run=False):
        self.create_count += 1
        bbl = feature['properties']['bbl']
        if dry_run:
            self.stdout.write('Create lot for bbl %s' % bbl)
            lot = None
        else:
            # Delete waterfront lots on the same parcel
            Lot.objects.filter(bbl=bbl, commons_type='waterfront').delete()

            if bbl and Lot.objects.filter(bbl=bbl).exists() and bbl.startswith('6'):
                # If a lot already exists with this fake bbl make a new fake bbl
                borough = feature['properties']['borough']
                bbl, block, lot = Lot.objects.fake_bbl(borough)
                feature['properties']['bbl'] = bbl
                feature['properties']['block'] = block
                feature['properties']['lot'] = lot

            lot = Lot.objects.create_lot_for_geom(
                GEOSGeometry(str(feature['geometry'])),
                **self.lot_kwargs(feature)
            )
            lot.save()
        return lot

    def delete_missing_lots(self, features, dry_run=False, **kwargs):
        pks = [int(f['properties']['pk']) for f in features]
        to_delete = Lot.objects.filter(
            remote=True,
            remote_locked=False,
            remote_site='llnyc',
        ).exclude(remote_pk__in=pks)
        self.delete_count += to_delete.count()

        if not dry_run:
            to_delete.delete()

    def lot_kwargs(self, feature):
        kwargs = {
            'added_reason': 'Lot is in Living Lots NYC',
            'address_line1': feature['properties'].get('address_line1', None),
            'address_line2': feature['properties'].get('address_line2', None),
            'bbl': feature['properties']['bbl'],
            'block': feature['properties']['block'],
            'borough': feature['properties']['borough'],
            'city': feature['properties'].get('city', None),
            'commons_type': 'vacant lot / garden',
            'known_use': self.get_use(feature),
            'known_use_certainty': feature['properties'].get('known_use_certainty', 0),
            'lot_number': feature['properties']['lot'],
            'name': feature['properties'].get('name', None),
            'owner': self.get_owner(feature),
            'postal_code': feature['properties'].get('postal_code', False),
            'remote': True,
            'remote_site': 'llnyc',
            'remote_pk': feature['properties']['pk'],
        }
        return kwargs

    def get_owner(self, feature):
        try:
            return Owner.objects.get_or_create(
                name=feature['properties']['owner_name'],
                defaults={
                    'owner_type': feature['properties']['owner_type'],
                }
            )[0]
        except KeyError:
            return None

    def get_use(self, feature):
        try:
            return Use.objects.get_or_create(
                name=feature['properties']['known_use'],
                visible=True
            )[0]
        except KeyError:
            return None

    def handle(self, *args, **options):
        self.load_lots(
            dry_run=options['dry-run'],
            verbosity=options['verbosity'],
        )
