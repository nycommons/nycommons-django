from hashlib import sha1
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class Participant(models.Model):
    """
    A person who is participating in something and who wishes to receive
    updates about the thing.
    """
    name = models.CharField(_('name'), max_length=256)
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    email_hash = models.CharField(max_length=40, null=True, blank=True,
                                  editable=False)
    added = models.DateTimeField(auto_now_add=True, editable=False)
    added_by = models.ForeignKey(User, null=True, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email_hash = sha1(settings.ORGANIZE_PARTICIPANT_SALT +
                                   self.email).hexdigest()
        super(Participant, self).save(*args, **kwargs)

    def get_edit_url(self):
        raise NotImplementedError('Implement Participant.get_edit_url()')


class BaseOrganizer(Participant):
    """
    Someone publicly participating in something.
    """
    # so we can do spatial joins between Organizer and Lot
    objects = models.GeoManager()

    type = models.ForeignKey('livinglots_organize.OrganizerType')
    url = models.URLField(_('url'), null=True, blank=True)
    notes = models.TextField(_('notes'), null=True, blank=True)
    facebook_page = models.CharField(
        _('facebook page'),
        max_length=256,
        null=True,
        blank=True,
        help_text=('The Facebook page for your organization. Please do not '
                   'enter your personal Facebook page.'),
    )
    post_publicly = models.BooleanField(_('post publicly'),
        default=True,
        help_text=_("Check this if you want to share your information on the "
                    "lot's page so that your neighbors can reach you and work "
                    "for access together. (If you don't click it, we'll just "
                    "send you updates but keep your information hidden.)"),
    )

    def recent_change_label(self):
        return 'new organizer: %s' % self.name

    def get_absolute_url(self):
        return "%s#organizer-%d" % (self.content_object.get_absolute_url(), self.pk)

    @classmethod
    def participation_adjective(cls):
        return 'organized'

    class Meta:
        abstract = True
        permissions = (
            ('email_organizers', 'Can send an email to all organizers'),
        )


class BaseWatcher(Participant):
    """
    Someone who is privately participating in something.
    """
    # so we can do spatial joins between Watcher and Lot
    objects = models.GeoManager()

    def recent_change_label(self):
        return 'new watcher'

    @classmethod
    def participation_adjective(cls):
        return 'watched'

    class Meta:
        abstract = True


class OrganizerType(models.Model):
    """
    A type of organizer (eg, individual, non-profit, governmental agency, ...).
    """
    name = models.CharField(max_length=64)
    is_group = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


def get_participant_models():
    def get_concrete_subclasses(model):
        if model._meta.abstract:
            parts = [get_concrete_subclasses(s) for s in model.__subclasses__()]
            if parts:
                return reduce(lambda a, b: a + b, parts)
            return tuple()
        else:
            return (model,)
    return get_concrete_subclasses(Participant)
