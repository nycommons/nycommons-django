from django.template import Context, Template
from django.views.generic import DetailView

from braces.views import (CsrfExemptMixin, LoginRequiredMixin,
                          PermissionRequiredMixin)

from .models import Mailing


class Preview(CsrfExemptMixin, LoginRequiredMixin, PermissionRequiredMixin,
              DetailView):
    model = Mailing
    permission_required = 'livinglots_mailings.change_mailing'
    template_name = 'livinglots/mailings/preview.html'

    def get_context_data(self, object=None, **kwargs):
        context = super(Preview, self).get_context_data(**kwargs)

        # Find potential recipients
        target_model = object.target_types.all()[0].model_class()
        recipients = [target_model.objects.all().order_by('?')[0],]

        # Find mailer and update context
        context.update(self.get_mailer().get_context(recipients))
        return context

    def get_mailer(self):
        """
        Get the mailer for this mailing.
        
        Only works on subclasses of Mailing, so we loop over them.
        """
        for cls in Mailing.__subclasses__():
            try:
                return cls.objects.get(pk=self.object.pk).get_mailer()
            except cls.DoesNotExist:
                continue
        return None

    def render_content(self, content, context):
        return Template(content).render(Context(context))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # NB: Using POST just in case the passed flatblock content is too long
        content = request.POST.get('content', None)
        context = self.get_context_data(object=self.object)
        context['content'] = self.render_content(content, context)
        return self.render_to_response(context)
