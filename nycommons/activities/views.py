from livinglots_activities.views import BaseActivityJSONListView
from livinglots_usercontent.notes.models import Note


class ActivityJSONListView(BaseActivityJSONListView):
    
    def get_action_dict(self, action):
        """Override to get details for notes"""
        d = super(ActivityJSONListView, self).get_action_dict(action)
        if action.target:
            d['target_url'] = action.target.get_absolute_url()
        if action.action_object and type(action.action_object) is Note:
            d['details'] = action.action_object.text
        return d
