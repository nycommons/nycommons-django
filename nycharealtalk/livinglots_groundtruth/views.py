from django.views.generic import CreateView

from braces.views import FormValidMessageMixin
from django_monitor.views import MonitorMixin

from livinglots_genericviews.views import AddGenericMixin


class BaseAddGroundtruthRecordView(FormValidMessageMixin, MonitorMixin,
                                   AddGenericMixin, CreateView):

    def get_form_valid_message(self):
        return 'Correction added successfully.'

    def get_success_url(self):
        return self.get_content_object().get_absolute_url()

    def get_template_names(self):
        return ['livinglots/groundtruth/add_groundtruthrecord.html',]
