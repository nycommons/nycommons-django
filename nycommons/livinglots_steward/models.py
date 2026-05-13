from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from livinglots_organize.models import BaseOrganizer


class OptedInStewardProjectManager(models.Manager):
    """
    A manager that only returns StewardProject instances where the group asked
    to be included on the map.
    """

    def get_queryset(self):
        return super(OptedInStewardProjectManager, self).get_queryset().filter(
            include_on_map=True,
        )


class StewardProjectMixin(models.Model):
    objects = models.Manager()
    opted_in = OptedInStewardProjectManager()

    project_name = models.CharField(_('project name'),
        max_length=256,
        help_text=_('The name of the project using this lot.'),
    )
    use = models.ForeignKey('livinglots_lots.Use',
        limit_choices_to={'visible': True},
        help_text=_('How is the project using the land?'),
        verbose_name=_('use'),
    )
    support_organization = models.CharField(_('support organization'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_("What is your project's support organization, if any?"),
    )
    land_tenure_status = models.CharField(_('land tenure status'),
        choices=(
            ('owned', _('project owns the land')),
            ('licensed', _('project has a license for the land')),
            ('lease', _('project has a lease for the land')),
            ('access', _('project has access to the land')),
            ('not sure', _("I'm not sure")),
        ),
        default=_('not sure'),
        max_length=50,
        help_text=_('What is the land tenure status for the project? (This '
                    'will not be shared publicly.)'),
    )
    include_on_map = models.BooleanField(_('include on map'),
        default=True,
        help_text=_('Can we include the project on our map?'),
    )

    class Meta:
        abstract = True


class BaseStewardProject(StewardProjectMixin):
    started_here = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class BaseStewardNotification(StewardProjectMixin, BaseOrganizer):
    """
    A notification from someone who is part of a stewarding project letting us
    know that they are stewards on a given lot.
    """

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
