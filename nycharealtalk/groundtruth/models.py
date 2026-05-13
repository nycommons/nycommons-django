from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_monitor.models import MonitoredObjectManager, MonitoredObjectMixin
        

from livinglots_groundtruth.models import BaseGroundtruthRecord


class GroundtruthRecord(MonitoredObjectMixin, BaseGroundtruthRecord):
    use = models.ForeignKey('livinglots_lots.Use',
        verbose_name=_('use'),
        limit_choices_to={'visible': False},
        blank=True,
        null=True,
    )

    objects = MonitoredObjectManager()
