from django.views.generic import ListView

from actstream.models import Action
from braces.views import JSONResponseMixin


class BaseActivityListView(ListView):
    model = Action
    paginate_by = 4
    template_name = 'livinglots/activities/activity_list.html'


class BaseActivityJSONListView(JSONResponseMixin, ListView):
    model = Action
    paginate_by = 10

    def get_pagination_dict(self, paginator, page_obj):
        d = {
            'pages': paginator.num_pages,
            'page': page_obj.number,
        }
        try:
            d['next_page'] = page_obj.next_page_number()
        except Exception:
            pass
        return d

    def get_action_dict(self, action):
        return {
            'action_object': str(action.action_object),
            'action_object_type': type(action.action_object).__name__,
            'action_object_url': action.action_object_url(),
            'actor': action.actor.username,
            'target': str(action.target),
            'target_url': action.target_url(),
            'timestamp': action.timestamp,
            'verb': action.verb,
        }

    def get(self, request, *args, **kwargs):
        super(BaseActivityJSONListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        paginator = context['paginator']
        page_obj = context['page_obj']
        return self.render_json_response({
            'actions': [self.get_action_dict(a) for a in context['object_list']],
            'pagination': self.get_pagination_dict(paginator, page_obj),
        })
