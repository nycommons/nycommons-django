from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from livinglots import get_owner_model_name


class BasePathwayManager(models.Manager):

    def get_for_lot(self, lot):
        pathways = self.all()
        if not lot or not lot.owner:
            return self.none()

        # Ownership filters
        if lot.owner.owner_type == 'private':
            pathways = pathways.filter(
                (Q(specific_private_owners__isnull=True) |
                 Q(specific_private_owners=lot.owner)),
                private_owners=True
            )
        elif lot.owner.owner_type == 'public':
            # Public lots: get pathways for public owners and pathways that
            # either do not specify certain public owners or match the given
            # lot's owner
            pathways = pathways.filter(
                (Q(specific_public_owners__isnull=True) |
                 Q(specific_public_owners=lot.owner)),
                public_owners=True
            )
        return pathways


class BasePathway(models.Model):
    objects = BasePathwayManager()

    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), max_length=256)
    is_active = models.BooleanField(_('is active'), default=True,
                                    db_index=True)
    author = models.ForeignKey(User, verbose_name=_('author'), null=True,
                               blank=True)
    order = models.PositiveIntegerField(default=10)

    # Filters for determining which lots a pathway can apply to
    private_owners = models.BooleanField(_('private owners'),
        default=False,
        help_text=_('This pathway applies to lots with private owners.'),
    )
    specific_private_owners = models.ManyToManyField(get_owner_model_name(),
        blank=True,
        limit_choices_to={'owner_type': 'private',},
        related_name='private+',
        help_text=_('This pathway applies to lots with these private owners.'),
    )
    public_owners = models.BooleanField(_('public owners'),
        default=False,
        help_text=_('This pathway applies to lots with public owners.'),
    )
    specific_public_owners = models.ManyToManyField(get_owner_model_name(),
        blank=True,
        limit_choices_to={'owner_type': 'public',},
        related_name='public+',
        help_text=_('This pathway applies to lots with these public owners.'),
    )

    class Meta:
        abstract = True
        ordering = ('order', 'name',)

    def __unicode__(self):
        return self.name
