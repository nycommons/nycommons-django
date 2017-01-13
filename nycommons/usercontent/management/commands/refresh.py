import dateutil.parser
import requests

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from actstream.models import Action

from lots.models import Lot


class UsercontentRefreshCommand(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(UsercontentRefreshCommand, self).__init__(*args, **kwargs)
        self.count = 0
        self.create_count = 0
        self.created = []
        self.delete_count = 0
        self.deleted_locally_count = 0
        self.no_lot_count = 0
        self.update_count = 0

        self.lot_content_type = ContentType.objects.get_for_model(Lot)

        self.user_content_type = ContentType.objects.get_for_model(User)
        self.default_actor = User.objects.get(pk=settings.ACTIVITY_STREAM_DEFAULT_ACTOR_PK)

        # Get most recently added remote object
        try:
            self.most_recent_added = self.local_model.objects.filter(
                remote=True,
                remote_site=self.remote_site,
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

    def load_remote_objects(self, dry_run=False, verbosity=1, **kwargs):
        remote_objects_json = self.get_json(verbosity=verbosity)
        for remote_object in remote_objects_json[self.remote_object_key]:
            self.count += 1
            self.load_remote_object_from_json(remote_object, dry_run=dry_run,
                    verbosity=verbosity, **kwargs)
        self.delete_missing_local_objects(remote_objects_json[self.remote_object_key],
                dry_run=dry_run, verbosity=verbosity, **kwargs)

        if verbosity > 0:
            self.print_report()

    def print_report(self):
        self.stdout.write('\nDone! Loaded %d %s objects' % (self.count,
            self.local_model._meta.model_name))
        self.stdout.write('-------------------------------')
        self.stdout.write('Created: %d' % self.create_count)
        self.stdout.write('Deleted: %d' % self.delete_count)
        self.stdout.write('Updated: %d' % self.update_count)
        self.stdout.write('No lot found: %d' % self.no_lot_count)
        self.stdout.write('Deleted locally but still exist on remote: %d' %
                self.deleted_locally_count)

    def get_json(self, verbosity=1):
        """
        Get JSON from remote site
        """
        url = self.remote_url
        key = settings.REMOTE_LOTS['llnyc']['api_key']
        request = requests.get(url + '?key=%s' % key)
        if verbosity >= 2:
            self.stdout.write('Loaded %s with status code %d' % (
                url, request.status_code
            ))
        return request.json()

    def load_remote_object_from_json(self, object_json, verbosity=1, **kwargs):
        """Load / update a remote object from json."""
        if verbosity >= 3:
            self.stdout.write(str(object_json))
        local_object = self.get_local_object(object_json)
        try:
            if local_object:
                if not local_object.remote_locked:
                    local_object = self.update_local_object(local_object,
                            object_json,
                            **kwargs)
            else:
                local_object = self.create_local_object(object_json,
                        verbosity=verbosity, **kwargs)
        except Lot.DoesNotExist:
            self.no_lot_count += 1
            self.stdout.write('Tried to add %s (%d) to nonexistent remote lot' % (
                self.local_model._meta.model_name,
                object_json['pk'],
            ))
        return local_object

    def get_local_object(self, object_json):
        try:
            return self.local_model.objects.get(
                remote=True,
                remote_site=self.remote_site,
                remote_pk=object_json['pk'],
            )
        except self.local_model.DoesNotExist:
            return None

    def update_local_object(self, local_object, object_json, dry_run=False):
        self.update_count += 1
        if dry_run:
            self.stdout.write('Update %s %d' % (
                self.local_model._meta.model_name,
                lot.pk,
            ))
        else:
            kwargs = self.object_kwargs(object_json)
            self.local_model.objects.filter(pk=local_object.pk).update(**kwargs)
        return local_object

    def create_local_object(self, object_json, dry_run=False, verbosity=1,
            **kwargs):
        added = dateutil.parser.parse(object_json['added'])
        if self.most_recent_added and self.most_recent_added > added:
            self.deleted_locally_count += 1
            if verbosity > 1:
                self.stdout.write('Skipping, seems like it was deleted locally')
            return
        pk = object_json['pk']
        if dry_run:
            self.create_count += 1
            self.stdout.write('Create %s for pk %s' % (
                self.local_model._meta.model_name,
                pk,
            ))
            local_object = None
        else:
            local_object = self.local_model(
                **self.object_kwargs(object_json)
            )
            local_object.save()
            self.created.append(local_object)
            self.update_action(local_object, object_json)
            self.create_count += 1
        return local_object

    def update_action(self, local_object, object_json):
        """
        Ensure that the action created for the object gets the correct timestamp
        """
        added = object_json['added']
        local_object.action_object_actions.update(
            actor_content_type=self.user_content_type,
            actor_object_id=self.default_actor.pk,
            timestamp=added
        )
        self.local_model.objects.filter(pk=local_object.pk).update(added=added)

    def delete_missing_local_objects(self, objects_json, dry_run=False, **kwargs):
        """
        Delete objects that are no longer on the remote site
        """
        pks = [int(o['pk']) for o in objects_json]
        to_delete = self.local_model.objects.filter(
            remote=True,
            remote_locked=False,
            remote_site=self.remote_site,
        ).exclude(remote_pk__in=pks)
        self.delete_count += to_delete.count()

        if not dry_run:
            to_delete.delete()

    def object_kwargs(self, object_json):
        """
        Get kwargs for creating and updating the given object based on its JSON
        representation
        """
        target_object_model = apps.get_model(*object_json['content_type'].split('.'))
        target_object = target_object_model.objects.get(
            remote=True,
            remote_site=self.remote_site,
            remote_pk=object_json['object_id']
        )
        target_content_type = ContentType.objects.get_for_model(target_object_model)

        kwargs = {
            'added': object_json['added'],
            'added_by_name': object_json['added_by_name'],
            'content_type_id': target_content_type.pk,
            'object_id': target_object.pk,
            'remote': True,
            'remote_site': self.remote_site,
            'remote_pk': object_json['pk'],
        }
        return kwargs

    def handle(self, *args, **options):
        self.load_remote_objects(
            dry_run=options['dry-run'],
            verbosity=options['verbosity'],
        )
