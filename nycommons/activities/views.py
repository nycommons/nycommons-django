from django.contrib.contenttypes.models import ContentType

from actstream.models import Action

from livinglots_activities.views import BaseActivityJSONListView
from livinglots_usercontent.files.models import File
from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.photos.models import Photo

from lots.models import Lot


class ActivityJSONListView(BaseActivityJSONListView):

    def get_action_dict(self, action):
        """Override to get details for notes"""
        d = super(ActivityJSONListView, self).get_action_dict(action)
        if action.target:
            d['target_url'] = action.target.get_absolute_url()
        if action.action_object and type(action.action_object) is File:
            d['file_url'] = action.action_object.document.url
        if action.action_object and type(action.action_object) is Note:
            d['details'] = action.action_object.text
        if action.action_object and type(action.action_object) is Photo:
            d['thumbnail_url'] = action.action_object.thumbnail.url
        return d


class PathwayActivityJSONListView(ActivityJSONListView):
    """
    View of activities that apply to a given pathway.
    """

    def get_queryset(self):
        # Get pathway
        pathway_app = self.request.GET.get('app')
        pathway_model = self.request.GET.get('model')
        pathway_id = self.request.GET.get('id')

        pathway_content_type = ContentType.objects.get(
            app_label=pathway_app,
            model=pathway_model
        )
        pathway = pathway_content_type.model_class().objects.get(pk=pathway_id)

        # Get lots for pathway
        lot_pks = pathway.lots.values_list('pk', flat=True)

        # Get actions for lots
        return Action.objects.filter(
            target_content_type=ContentType.objects.get_for_model(Lot),
            target_object_id__in=[str(pk) for pk in lot_pks],
        )
