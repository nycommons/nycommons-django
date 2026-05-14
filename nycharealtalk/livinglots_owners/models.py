from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from livinglots import get_owner_model_name, get_owner_contact_model_name


class OwnerManager(models.Manager):

    def get_or_create(self, name, defaults={}, ignorecase=True):
        """Get or create an owner while taking aliases into account."""
        try:
            if ignorecase:
                try:
                    return self.get(name__iexact=name), False
                except MultipleObjectsReturned:
                    return self.get(name__exact=name), False
            else:
                return self.get(name__exact=name), False
        except ObjectDoesNotExist:
            try:
                return self.get(aliases__name__iexact=name), False
            except MultipleObjectsReturned:
                return self.get(aliases__name__exact=name), False
            except ObjectDoesNotExist:
                obj = self.create(name=name, **defaults)
                return obj, True


@python_2_unicode_compatible
class Alias(models.Model):
    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('alias')
        verbose_name_plural = _('aliases')


@python_2_unicode_compatible
class BaseOwner(models.Model):

    objects = OwnerManager()

    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )

    OWNER_TYPE_CHOICES = (
        ('private', 'private'),
        ('public', 'public'),
        ('unknown', 'unknown'),
    )
    owner_type = models.CharField(_('owner type'),
        choices=OWNER_TYPE_CHOICES,
        default='private',
        max_length=20,
    )

    aliases = models.ManyToManyField('livinglots_owners.Alias',
        help_text=_('Other names for this owner'),
        verbose_name=_('aliases'),
        blank=True,
    )

    default_contact = models.ForeignKey(get_owner_contact_model_name(),
        blank=True,
        null=True,
        related_name='+',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '%s (%s)' % (self.name, self.owner_type)

    def add_alias(self, alias_name):
        alias, created = Alias.objects.get_or_create(name=alias_name)
        self.aliases.add(alias)
        return alias

    def make_alias(self, other_owner):
        """Make other_owner an alias for this owner."""

        # redirect all relationships to this owner
        for field in self._meta.get_fields():
            # Field has no related model, skip it
            if not field.related_model: continue
            try:
                field.related_model.objects.filter(owner=other_owner).update(owner=self)
            except FieldError:
                # Related model has no owner field, skip it
                pass

        # redirect aliases to this owner
        for alias in other_owner.aliases.all():
            self.aliases.add(alias)
        self.add_alias(other_owner.name)

        # get rid of the other owner
        other_owner.delete()


@python_2_unicode_compatible
class BaseOwnerContact(models.Model):
    """
    A base class for a person at an owning entity (eg, a city agency) who you
    can contact to talk about a piece of land.
    """
    owner = models.ForeignKey(get_owner_model_name())
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class BaseOwnerGroup(models.Model):
    name = models.CharField(max_length=256)

    OWNER_TYPE_CHOICES = (
        ('private', 'private'),
        ('public', 'public'),
        ('unknown', 'unknown'),
    )
    owner_type = models.CharField(_('owner type'),
        choices=OWNER_TYPE_CHOICES,
        default='private',
        max_length=20,
    )

    owners = models.ManyToManyField(get_owner_model_name())

    class Meta:
        abstract = True
        ordering = ['name',]

    def __str__(self):
        return '%s (%s)' % (self.name, self.owner_type)
