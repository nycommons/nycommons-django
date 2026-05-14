from django.views.generic import CreateView

from braces.views import FormValidMessageMixin

from livinglots_genericviews.views import AddGenericMixin


class AddContentView(FormValidMessageMixin, AddGenericMixin, CreateView):

    def _get_content_name(self):
        return self.form_class._meta.model._meta.object_name

    def get_form_valid_message(self):
        return '%s added successfully.' % self._get_content_name()

    def get_form_kwargs(self):
        kwargs = super(AddContentView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super(AddContentView, self).get_initial()
        user = self.request.user

        # If user has name, set that for them
        try:
            initial['added_by_name'] = user.first_name or user.username
        except AttributeError:
            pass
        return initial

    def get_success_url(self):
        return self.get_content_object().get_absolute_url()

    def get_template_names(self):
        return [
            'livinglots/usercontent/add_%s.html' % self._get_content_name().lower(),
        ]

    def form_valid(self, form):
        """
        Save the content and notify participants who are following the target
        lot.
        """
        self.object = form.save()

        # NB: Notifications are sent to followers using a descendant of
        # NotifyParticipantsOnCreationForm 
        return super(AddContentView, self).form_valid(form)
