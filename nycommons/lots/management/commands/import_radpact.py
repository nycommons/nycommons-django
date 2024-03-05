import csv
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from lots.models import Lot

class Command(BaseCommand):
    help = 'Import RAD/PACT data'

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
        name = row['Development Name']
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

    def lot_kwargs(self, row):
        status = row['Status']
        converted = status in ('Construction Complete', 'Under Construction')

        date = None
        date_str = row['Conversion Date / Anticipated Conversion Date']
        try:
            date = datetime.strptime(date_str, '%Y')
        except ValueError:
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
            except ValueError:
                pass

        kwargs = {
            'radpact_converted': converted,
            'radpact_planned': not converted,
            'radpact_status': status,
            'radpact_conversion_date': date,
            'radpact_developers': row['Developer(s)'],
            'radpact_general_contractor': row['General Contractor'],
            'radpact_property_manager': row['Property Manager'],
            'radpact_social_service_provider': row['Social Service Provider'],
        }
        return kwargs

    def get_lot(self, row):
        # Only public housing with no group, name matches
        try:
            return Lot.objects.get(
                commons_type='public housing',
                group__isnull=True,
                name__iexact=row['Development Name'],
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
