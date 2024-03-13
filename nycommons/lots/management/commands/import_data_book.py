import csv
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from lots.models import Lot

class Command(BaseCommand):
    help = 'Import Data Book data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.found = []
        self.not_found = []

    def add_arguments(self, parser):
        parser.add_argument('input_file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            default=False,
            help='Perform a dry-run',
        )

    def handle(self, *args, **options):
        input_file = self.load_input_file(options['input_file'])
        self.join_data(
            input_file,
            dry_run=options['dry-run'],
            verbosity=options['verbosity'],
        )

    def load_input_file(self, filename):
        reader = csv.DictReader(open(filename, 'rb'))
        return [r for r in reader]

    def join_data(self, input_file, verbosity=1, **kwargs):
        for row in input_file:
            self.update_lot_from_row(row, verbosity=verbosity, **kwargs)

        if verbosity > 0:
            self.print_report()

    def update_lot_from_row(self, row, verbosity=1, **kwargs):
        if verbosity >= 3:
            self.stdout.write(str(row))
        lot = self.get_lot(row)
        name = row['DEVELOPMENT']
        if lot:
            lot = self.update_lot(lot, row, **kwargs)
            self.found.append(name)
        else:
            self.not_found.append(name)
        return lot

    def update_lot(self, lot, row, dry_run=False):
        kwargs = self.lot_kwargs(row)
        if dry_run:
            self.stdout.write('Update lot %d' % lot.pk)
        else:
            Lot.objects.filter(pk=lot.pk).update(**kwargs)
        return lot

    def get_int(self, v):
        if v == '':
            return None
        else:
            return int(v.split('.')[0].replace(',', ''))

    def get_float(self, v):
        if v == '':
            return None
        else:
            return float(v.replace(',', '').replace('%', '').replace('$', ''))

    def lot_kwargs(self, row):
        kwargs = {
            'current_units': self.get_int(row['NUMBER OF CURRENT APARTMENTS']),
            'total_units': self.get_int(row['TOTAL NUMBER OF APARTMENTS']),
            'rental_rooms': self.get_int(row['NUMBER OF RENTAL ROOMS']),
            'population_section_8': self.get_int(row['POPULATION SECTION 8 TRANSITION']),
            'population_public_housing': self.get_int(row['POPULATION PUBLIC HOUSING']),
            'population_total': self.get_int(row['TOTAL POPULATION']),
            'families_fixed_income': self.get_int(row['TOTAL # OF FIXED INCOME HOUSEHOLD']),
            'families_fixed_income_percent': self.get_float(
                row['PERCENT FIXED INCOME HOUSEHOLDS']
            ),
            'buildings_residential': self.get_int(row['NUMBER OF RESIDENTIAL BLDGS']),
            'buildings_nonresidential': self.get_int(
                row['NUMBER OF NON-RESIDENTIAL BLDGS']
            ),
            'buildings_stories': row['NUMBER OF STORIES'],
            'total_area': self.get_float(row['TOTAL AREA SQ FT']),
            'building_land_coverage': self.get_float(row['BLDG COVERAGE %']),
            'density': self.get_float(row['DENSITY']),
            'cost_total': self.get_float(row['DEVELOPMENT COST']),
            'cost_per_room': self.get_float(row['PER RENTAL ROOM']),
            'rent_avg': self.get_float(row['AVG MONTHLY GROSS RENT']),
            'senior_development': row['SENIOR DEVELOPMENT'],
            'electricity_residents': row['ELECTRICITY PAID BY RESIDENTS'] == 'YES',
        }
        return kwargs

    def get_lot(self, row):
        # Only public housing with no group, name matches
        try:
            return Lot.objects.get(
                commons_type='public housing',
                group__isnull=True,
                name__iexact=row['DEVELOPMENT'],
            )
        except Lot.DoesNotExist:
            return None

    def print_report(self):
        self.stdout.write('\nDone!')

        self.stdout.write('Found %d lots' % len(self.found))
        for lot in self.found:
            self.stdout.write('\t' + lot)

        self.stdout.write('Could not find %d lots' % len(self.not_found))
        for lot in self.not_found:
            self.stdout.write('\t' + lot)
