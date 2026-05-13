"""
Generic views for editing participants.

"""

from django.apps import apps
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import Context, Template
from django.views.generic import CreateView, TemplateView, View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import DeleteView

from braces.views import (CsrfExemptMixin, LoginRequiredMixin,
                          StaffuserRequiredMixin)

from livinglots import (get_organizer_model, get_organizer_model_name,
                        get_watcher_model)
from livinglots_genericviews.views import AddGenericMixin

from .mail import get_target_participant_context


class EditParticipantMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        hash = self.get_participant_hash()
        context = super(EditParticipantMixin, self).get_context_data(**kwargs)
        context.update({
            'organizers': get_organizer_model().objects.filter(email_hash__istartswith=hash).order_by('added'),
        })
        if get_watcher_model():
            context['watchers'] = get_watcher_model().objects.filter(email_hash__istartswith=hash).order_by('added')
        return context

    def get_participant_hash(self):
        raise NotImplementedError('Implement get_participant_hash() to use '
                                  'EditParticipantMixin.')


class DeleteParticipantView(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(DeleteParticipantView, self).get_context_data(**kwargs)
        context['target'] = self.object.content_object
        context['next_url'] = self.request.GET.get('next_url')
        return context

    def get_success_url(self):
        messages.info(self.request, self._get_success_message())
        return self.request.POST.get(
            'next_url',
            self.object.content_object.get_absolute_url()
        )

    def _get_success_message(self):
        verb = 'working on'
        if isinstance(self.object, get_organizer_model()):
            verb = 'subscribed to'
        return 'You are no longer %s %s.' % (verb, self.object.content_object)


class DeleteOrganizerView(DeleteParticipantView):
    model = get_organizer_model()
    pk_url_kwarg = 'organizer_pk'
    template_name = 'livinglots/organize/organizer_confirm_delete.html'


class DeleteWatcherView(DeleteParticipantView):
    model = get_watcher_model()
    pk_url_kwarg = 'watcher_pk'
    template_name = 'livinglots/organize/watcher_confirm_delete.html'


class EditLotParicipantView(EditParticipantMixin, TemplateView):
    template_name = 'livinglots/organize/edit_participant.html'

    def get_context_data(self, **kwargs):
        context = super(EditLotParicipantView, self).get_context_data(**kwargs)
        context.update({
            'email': self._get_email(context),
        })
        return context

    def get_participant_hash(self):
        return self.kwargs['hash']

    def _get_email(self, context):
        try:
            return context['organizers'][0].email
        except Exception:
            try:
                return context['watchers'][0].email
            except Exception:
                return None


class ParticipantMixin(object):

    def _get_participant_type(self):
        return self.model._meta.object_name.lower()


class AddParticipantView(AddGenericMixin, ParticipantMixin, CreateView):

    def get_success_url(self):
        kwargs = {
            'object_pk': self.object.pk,
            'hash': self.object.email_hash[:30],
            'pk': self.object.object_id,
        }
        urlname = 'organize:add_%s_success' % self._get_participant_type()
        return reverse(urlname, kwargs=kwargs)

    def get_template_names(self):
        return [
            'livinglots/organize/add_%s.html' % self._get_participant_type(),
        ]


class AddParticipantSuccessView(ParticipantMixin, TemplateView):
    model = get_organizer_model()

    def get_context_data(self, **kwargs):
        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        try:
            context['participant'] = self.model.objects.filter(
                email_hash__istartswith=kwargs['hash'],
                pk=self.kwargs['object_pk'],
            )[0]
        except Exception:
            raise Http404
        return context

    def get_template_names(self):
        return [
            'livinglots/organize/add_%s_success.html' % (
                self._get_participant_type(),
            ),
        ]


class NotificationPreview(CsrfExemptMixin, LoginRequiredMixin,
                          StaffuserRequiredMixin, TemplateResponseMixin, View):
    template_name = 'livinglots/organize/notifications/preview.html'

    obj_types = {
        'file': 'files.File',
        'note': 'notes.Note',
        'organizer': get_organizer_model_name(),
        'photo': 'photos.Photo',
    }

    def get_object(self, slug):
        """
        Get the object that the participant is getting a notification about.

        This is the thing that was posted recently and triggered the
        notification.
        """
        # XXX this could go wrong in a few big ways
        new_obj_name = self.obj_types[slug.split('new_')[-1]]
        new_obj_model = apps.get_model(*new_obj_name.split('.'))
        return new_obj_model.objects.order_by('?')[0]

    def get_participant(self, target):
        """Attempt to get a participant on this target"""
        return get_organizer_model().objects.filter(
            content_type_id=ContentType.objects.get_for_model(target).pk,
            object_id=target.pk,
        )[0]

    def get_context_data(self, slug):
        # Are we even in the right place?
        if not slug.startswith('organize.notifications'):
            return {}

        # Get an object using slug kwarg
        obj = self.get_object(slug)

        # Get a theoretical participant, trying to match to the given target
        participant = self.get_participant(obj.content_object)

        # Get context using the mailing context
        return get_target_participant_context(participant, obj)

    def render_content(self, content, context):
        return Template(content).render(Context(context))

    def post(self, request, *args, **kwargs):
        # NB: Using POST just in case the passed flatblock content is too long
        content = request.POST.get('content', None)
        context = self.get_context_data(kwargs.get('slug', None))
        context['content'] = self.render_content(content, context)
        return self.render_to_response(context)
