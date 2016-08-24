import dateutil.parser
import requests

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_mailings.models import Mailing
from livinglots_organize.models import OrganizerType

from lots.models import Lot
from organize.models import Organizer


class Command(BaseCommand):
    help = 'Refresh organize data from LLNYC'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.count = 0
        self.create_count = 0
        self.created = []
        self.delete_count = 0
        self.deleted_locally_count = 0
        self.update_count = 0

        self.lot_content_type = ContentType.objects.get_for_model(Lot)

        # Get most recently added remote organizer
        try:
            self.most_recent_added = Organizer.objects.filter(
                remote=True,
                remote_site='llnyc',
            ).order_by('-added')[0].added
        except IndexError:
            self.most_recent_added = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            default=False,
            help='Perform a dry-run',
        )

    def load_organizers(self, dry_run=False, verbosity=1, **kwargs):
        organizers_json = self.get_json(verbosity=verbosity)
        for organizer in organizers_json['organizers']:
            self.count += 1
            self.load_organizer_from_json(organizer, dry_run=dry_run,
                    verbosity=verbosity, **kwargs)
        self.delete_missing_organizers(organizers_json['organizers'],
                dry_run=dry_run, verbosity=verbosity, **kwargs)

        if not dry_run:
            self.fake_mailings(self.created, verbosity=verbosity, **kwargs)

        if verbosity > 0:
            self.print_report()

    def fake_mailings(self, created, verbosity=1, **kwargs):
        """
        Fake mailings for the organizers we created.

        Avoid spammy email to old organizers.
        """
        if verbosity == 1:
            self.stdout.write('Faking mailings')
        for mailing in Mailing.objects.all().select_subclasses():
            if verbosity > 1:
                self.stdout.write('Faking mailing %s' % mailing)
            mailer = mailing.get_mailer()
            mailer.add_delivery_records(created, sent=True)

    def print_report(self):
        self.stdout.write('\nDone! Loaded %d organizers' % self.count)
        self.stdout.write('-------------------------------')
        self.stdout.write('Created: %d' % self.create_count)
        self.stdout.write('Deleted: %d' % self.delete_count)
        self.stdout.write('Updated: %d' % self.update_count)
        self.stdout.write('Deleted locally but still exist on remote: %d' %
                self.deleted_locally_count)

    def get_json(self, verbosity=1):
        url = settings.REMOTE_LOTS['llnyc']['api_organizers_url']
        key = settings.REMOTE_LOTS['llnyc']['api_key']
        request = requests.get(url + '?key=%s' % key)
        if verbosity >= 2:
            self.stdout.write('Loaded %s with status code %d' % (
                url, request.status_code
            ))
        return request.json()

    def load_organizer_from_json(self, organizer_json, verbosity=1, **kwargs):
        """Load / update a organizer from json."""
        if verbosity >= 3:
            self.stdout.write(str(organizer_json))
        organizer = self.get_organizer(organizer_json)
        try:
            if organizer:
                if not organizer.remote_locked:
                    organizer = self.update_organizer(organizer, organizer_json,
                            **kwargs)
            else:
                organizer = self.create_organizer(organizer_json,
                        verbosity=verbosity, **kwargs)
        except Lot.DoesNotExist:
            self.stdout.write('Tried to add organizer (%d) to nonexistent remote lot (%d)' % (
                organizer_json['pk'],
                organizer_json['lot_pk'],
            ))
        return organizer

    def get_organizer(self, organizer_json):
        try:
            return Organizer.objects.get(
                remote=True,
                remote_site='llnyc',
                remote_pk=organizer_json['pk'],
            )
        except Organizer.DoesNotExist:
            return None

    def update_organizer(self, organizer, organizer_json, dry_run=False):
        self.update_count += 1
        kwargs = self.organizer_kwargs(organizer_json)
        if dry_run:
            self.stdout.write('Update organizer %d' % lot.pk)
        else:
            Organizer.objects.filter(pk=organizer.pk).update(**kwargs)
        return organizer

    def create_organizer(self, organizer_json, dry_run=False, verbosity=1,
            **kwargs):
        organizer_added = dateutil.parser.parse(organizer_json['added'])
        if self.most_recent_added and self.most_recent_added > organizer_added:
            self.deleted_locally_count += 1
            if verbosity > 1:
                self.stdout.write('Skipping organizer, seems like it was deleted locally')
            return
        self.create_count += 1
        pk = organizer_json['pk']
        if dry_run:
            self.stdout.write('Create organizer for pk %s' % pk)
            organizer = None
        else:
            organizer = Organizer(
                **self.organizer_kwargs(organizer_json)
            )
            organizer.save()
            self.created.append(organizer)
        return organizer

    def delete_missing_organizers(self, organizers_json, dry_run=False, **kwargs):
        pks = [int(o['pk']) for o in organizers_json]
        to_delete = Organizer.objects.filter(
            remote=True,
            remote_locked=False,
            remote_site='llnyc',
        ).exclude(remote_pk__in=pks)
        self.delete_count += to_delete.count()

        if not dry_run:
            to_delete.delete()

    def organizer_kwargs(self, organizer_json):
        lot = Lot.objects.get(
            remote=True,
            remote_pk=organizer_json['lot_pk'],
            remote_site='llnyc',
        )
        kwargs = {
            'email': organizer_json.get('email', None),
            'email_hash': organizer_json.get('email_hash', None),
            'content_type': self.lot_content_type,
            'object_id': lot.pk,
            'name': organizer_json['name'],
            'notes': organizer_json.get('notes', None),
            'post_publicly': organizer_json.get('public', False),
            'phone': organizer_json.get('phone', None),
            'remote': True,
            'remote_site': 'llnyc',
            'remote_pk': organizer_json['pk'],
            'type': OrganizerType.objects.get_or_create(
                name=organizer_json['type']
            )[0],
        }
        return kwargs

    def handle(self, *args, **options):
        self.load_organizers(
            dry_run=options['dry-run'],
            verbosity=options['verbosity'],
        )
