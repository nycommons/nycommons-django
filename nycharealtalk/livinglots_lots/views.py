from datetime import date
import geojson
import json

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import (Http404, HttpResponseRedirect, HttpResponse,
                         HttpResponseBadRequest)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView, View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from dal import autocomplete
from braces.views import (CsrfExemptMixin, JSONResponseMixin, LoginRequiredMixin,
                          PermissionRequiredMixin)
from inplace.boundaries.models import Boundary
from inplace.views import (GeoJSONListView, GeoJSONResponseMixin, KMLView,
                           PlacesDetailView)
from livinglots import get_lot_model, get_lotgroup_model
from livinglots_genericviews.views import CSVView, JSONResponseView
from livinglots_organize.mail import mass_mail_organizers, mass_mail_watchers

from .exceptions import ParcelAlreadyInLot
from .forms import HideLotForm
from .models import Use
from .signals import lot_details_loaded


#
# Helper mixins
#

class FilteredLotsMixin(object):
    """A mixin that makes it easy to filter on Lots using a LotResource."""

    def get_lots(self):
        # Give the user a different set of lots based on their permissions
        return get_lot_model().get_filter()(self.request.GET,
                                            user=self.request.user)


class LotContextMixin(ContextMixin):

    def get_lot(self):
        """Get the lot referred to by the incoming request"""
        try:
            if self.request.user.has_perm('lots.view_all_lots'):
                return get_lot_model().objects.get(pk=self.kwargs['pk'])
            return get_lot_model().visible.get(pk=self.kwargs['pk'])
        except get_lot_model().DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(LotContextMixin, self).get_context_data(**kwargs)
        context['lot'] = self.get_lot()
        return context


class LotAddGenericMixin(FormMixin):
    """
    A mixin that eases adding content that references a single lot using
    generic relationships.
    """

    def get_initial(self):
        """Add initial content_type and object_id to the form"""
        initial = super(LotAddGenericMixin, self).get_initial()
        try:
            object_id = self.kwargs['pk']
        except KeyError:
            raise Http404
        initial.update({
            'content_type': ContentType.objects.get_for_model(get_lot_model()),
            'object_id': object_id,
        })
        return initial


class LotFieldsMixin(object):
    """
    A mixin that makes it easier to add a lot's fields to the view's output.
    """
    def get_fields(self):
        return self.fields

    def get_field_owner(self, lot):
        return lot.owner.name

    def get_field_owner_type(self, lot):
        return lot.owner.get_owner_type_display()

    def get_field_known_use(self, lot):
        return lot.known_use.name

    def _field_value(self, lot, field):
        try:
            # Call get_field_<field>()
            return getattr(self, 'get_field_%s' % field)(lot)
        except AttributeError:
            try:
                # Else try to get the property from the model instance
                return getattr(lot, field)
            except AttributeError:
                return None

    def _as_dict(self, lot):
        return dict([(f, self._field_value(lot, f)) for f in self.get_fields()])


class LotGeoJSONMixin(object):

    def get_feature(self, lot):
        if lot.known_use:
            layer = 'in use'
        elif lot.owner and lot.owner.owner_type == 'public':
            layer = 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            layer = 'private'
        else:
            layer = ''

        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot_geojson),
            properties={
                'pk': lot.pk,
                'layer': layer,
            },
        )


#
# Export views
#


class ExportMixin(object):

    def get_sitename(self):
        return ''

    def get_filename(self):
        return '%s lots %s' % (
            self.get_sitename(),
            date.today().strftime('%Y-%m-%d'),
        )


class LotsCSV(ExportMixin, LotFieldsMixin, FilteredLotsMixin, CSVView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'latitude', 'longitude', 'known_use', 'owner', 'owner_type',)

    def get_rows(self):
        for lot in self.get_lots().qs.distinct():
            yield self._as_dict(lot)


class LotsKML(ExportMixin, LotFieldsMixin, FilteredLotsMixin, KMLView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'known_use', 'owner', 'owner_type',)

    def get_context_data(self, **kwargs):
        return {
            'places': self.get_lots().qs.kml(),
            'download': True,
            'filename': self.get_filename(),
        }

    def render_to_response(self, context):
        return super(LotsKML, self).render_to_response(context)


class LotsGeoJSON(ExportMixin, LotFieldsMixin, FilteredLotsMixin,
                  GeoJSONResponseMixin, JSONResponseView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'known_use', 'owner', 'owner_type',)

    def get_context_data(self, **kwargs):
        return self.get_feature_collection()

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot.centroid.geojson),
            properties=self._as_dict(lot),
        )

    def get_queryset(self):
        return self.get_lots()

    def render_to_response(self, context):
        response = super(LotsGeoJSON, self).render_to_response(context)
        if self.request.GET.get('download', 'no') == 'yes':
            response['Content-Disposition'] = ('attachment; filename="%s.json"' %
                                               self.get_filename())
        return response


class LotsGeoJSONPolygon(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(polygon__isnull=False).geojson(
            field_name='polygon',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')


#
# Counting views
#

class LotsCountView(FilteredLotsMixin, JSONResponseView):

    def get_context_data(self, **kwargs):
        lots = self.get_lots()
        context = {
            'lots-count': lots.count(),
            'no-known-use-count': lots.qs.filter(known_use__isnull=True).count(),
            'in-use-count': lots.qs.filter(
                known_use__isnull=False,
                known_use__visible=True,
            ).count(),
        }
        return context


class LotsCountBoundaryView(JSONResponseView):

    def get_context_data(self, **kwargs):
        return self.get_counts()

    def get_filters(self):
        return get_lot_model().get_filter()(self.request.GET,
                                            user=self.request.user)

    def get_counts(self):
        boundary_layer = self.request.GET.get('choropleth_boundary_layer', '')
        lots = self.get_filters()

        boundaries = Boundary.objects.filter(
            layer__name=boundary_layer,
        )

        counts = {}
        for boundary in boundaries:
            counts[boundary.label] = lots.filter(
                centroid__within=boundary.simplified_geometry
            ).count()
        return counts


class LotsMap(TemplateView):
    template_name = 'livinglots/lots/map.html'

    def get_context_data(self, **kwargs):
        context = super(LotsMap, self).get_context_data(**kwargs)
        context.update({
            'filters': get_lot_model().get_filter()(self.request.GET,
                                                    user=self.request.user),
            'uses': Use.objects.all().order_by('name'),
        })
        return context


#
# Detail views
#

class LotDetailView(PlacesDetailView):
    model = get_lot_model()

    def get_object(self):
        lot = super(LotDetailView, self).get_object()
        if not (lot.is_visible or self.request.user.has_perm('lots.view_all_lots')):
            raise Http404
        return lot

    def get(self, request, *args, **kwargs):
        # Redirect to the lot's group, if it has one
        self.object = self.get_object()
        lot_details_loaded.send(sender=self, instance=self.object)
        if self.object.group:
            messages.info(request, _("The lot you requested is part of a "
                                     "group. Here is the group's page."))
            return HttpResponseRedirect(self.object.group.get_absolute_url())
        return super(LotDetailView, self).get(request, *args, **kwargs)


class LotGeoJSONDetailView(LotGeoJSONMixin, GeoJSONListView):
    model = get_lot_model()

    def get_queryset(self):
        lot = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.model.objects.find_nearby(lot, include_self=True, miles=.1)


#
# Lot creation views
#


class BaseCreateLotView(PermissionRequiredMixin, View):
    permission_required = 'lots.add_lot'

    def get_parcels(self, pks):
        raise NotImplementedError('Implement BaseCreateLotView.get_parcels()')

    def create_lot_for_parcels(self, pks, **lot_kwargs):
        parcels = self.get_parcels(pks)
        return get_lot_model().objects.create_lot_for_parcels(parcels, **lot_kwargs)

    def post(self, request, *args, **kwargs):
        parcel_pks = request.POST.get('pks')
        lot = None
        lot_kwargs = {
            'added_reason': 'Created using add-lot mode',
            'known_use_certainty': 10,
            'known_use_locked': True,
        }

        if parcel_pks:
            parcel_pks = parcel_pks.split(',')
            try:
                lot = self.create_lot_for_parcels(parcel_pks, **lot_kwargs)
            except ParcelAlreadyInLot:
                return HttpResponseBadRequest('One or more parcels already in lots')

        if lot:
            return HttpResponse('%s' % lot.pk, content_type='text/plain')
        else:
            return HttpResponseBadRequest('No lot created')


class BaseCreateLotByGeomView(View):

    def post(self, request, *args, **kwargs):
        geom = request.POST.get('geom')
        lot = None
        lot_kwargs = {
            'added_reason': 'Drawn using add-lot mode',
            'known_use_certainty': 10,
            'known_use_locked': True,
        }

        if geom:
            try:
                lot = get_lot_model().objects.create_lot_for_geoms(geom, **lot_kwargs)
            except ValueError:
                return HttpResponseBadRequest('Only polygons are allowed')

        if lot:
            return HttpResponse('%s' % lot.pk, content_type='text/plain')
        else:
            return HttpResponseBadRequest('No lot created')


class CreateLotByGeomView(BaseCreateLotByGeomView):
    permission_required = 'lots.add_lot'


class CheckLotWithParcelExistsView(PermissionRequiredMixin, View):
    permission_required = 'lots.add_lot'

    def get_by_parcel(self, pk):
        try:
            return get_lot_model().objects.get(parcel__pk=pk)
        except Exception:
            return None

    def get(self, request, *args, **kwargs):
        parcel_pk = kwargs.get('pk')
        lot = self.get_by_parcel(parcel_pk)
        if lot:
            return HttpResponse(lot.pk)
        else:
            return HttpResponse('None')


#
# Grouping
#


class AddToGroupView(CsrfExemptMixin, LoginRequiredMixin, 
                     PermissionRequiredMixin, JSONResponseMixin,
                     SingleObjectMixin, View):
    """
    A view for adding a lot to a group.

    This requires two POST parameters:
     * pk: the lot or lot group being added to
     * lot_to_add: the lot that is not currently in the group but will be after
       this view does its work
    """
    model = get_lot_model()
    permission_required = 'lots.add_lot'

    def get_success_message(self, to_add):
        msg = 'Successfully added %s to this group. ' % str(to_add)
        msg += ("You're <strong>not done yet</strong>: we've merged notes, "
                "photos, organizers, and other content, but you should check "
                "on the group's owner and known use information by clicking "
                "<strong>Edit this lot</strong>.")
        return msg

    def post(self, request, *args, **kwargs):
        lot = self.get_object()
        to_add = get_lot_model().objects.get(pk=request.POST.get('lot_to_add'))
        context = {
            'lot': lot.pk,
            'lot_to_add': to_add.pk,
            'group': lot.group_with(to_add).pk,
        }
        messages.success(request, self.get_success_message(to_add))
        return self.render_json_response(context)


class RemoveFromGroupView(CsrfExemptMixin, LoginRequiredMixin,
                          PermissionRequiredMixin, JSONResponseMixin,
                          SingleObjectMixin, View):
    """
    A view for removing a lot from a group.

    This requires two POST parameters:
     * pk: The lot to remove from its group. Lots can only be in one group at a
       time, so this should be sufficient.
    """
    model = get_lot_model()
    permission_required = 'lots.add_lot'

    def get_success_message(self, lot):
        return 'Successfully removed %s from this group. ' % lot

    def post(self, request, *args, **kwargs):
        lot = self.get_object()
        group = lot.group
        group.remove(lot)
        context = {
            'lot': lot.pk,
            'former_group': group.pk,
        }
        messages.success(request, self.get_success_message(lot))
        return self.render_json_response(context)


#
# Hide
#


class HideLotSuccessView(LotContextMixin, PermissionRequiredMixin,
                         TemplateView):
    permission_required = 'lots.change_lot'
    template_name = 'livinglots/lots/hide_success.html'


class HideLotView(LotContextMixin, PermissionRequiredMixin, FormView):
    form_class = HideLotForm
    permission_required = 'lots.change_lot'
    template_name = 'livinglots/lots/hide.html'

    def get_success_url(self):
        return reverse('lots:hide_lot_success', kwargs={
            'pk': self.get_lot().pk,
        })

    def get_initial(self):
        initial = super(HideLotView, self).get_initial()
        initial.update({
            'lot': self.get_lot(),
        })
        return initial

    def form_valid(self, form):
        lot = self.get_lot()
        lot.known_use = form.cleaned_data['use']
        lot.known_use_certainty = 10
        lot.known_use_locked = True
        lot.save()
        return super(HideLotView, self).form_valid(form)


#
# Email organizers views
#

class LotParticipantsMixin(FilteredLotsMixin):
    model = None
    participant_type = None

    def get_participants(self):
        lots = self.get_lots().qs.values_list('pk', flat=True)
        return self.model.objects.filter(
            content_type=ContentType.objects.get_for_model(get_lot_model()),
            object_id__in=lots,
        )


class CountParticipantsView(LoginRequiredMixin, PermissionRequiredMixin,
        JSONResponseMixin, LotParticipantsMixin, View):

    def get(self, request, *args, **kwargs):
        participants = self.get_participants()
        context = {
            'emails': len(set(participants.values_list('email', flat=True))),
            'participants': participants.count(),
        }
        context['%ss' % self.model.__name__.lower()] = participants.count()
        return self.render_json_response(context)


class EmailParticipantsView(LoginRequiredMixin, PermissionRequiredMixin,
        JSONResponseMixin, LotParticipantsMixin, View):

    def get(self, request, *args, **kwargs):
        participants = self.get_participants().exclude(email=None).exclude(email='')
        subject = request.GET.get('subject')
        text = request.GET.get('text')
        emails = set(participants.values_list('email', flat=True))
        if not (subject and text and emails):
            return HttpResponseBadRequest('All parameters are required')
        context = {
            'emails': len(emails),
            'participants': len(participants),
            'subject': subject,
            'text': text,
        }
        context['%ss' % self.model.__name__.lower()] = participants.count()

        if self.participant_type == 'organizer':
            mass_mail_organizers(subject, text, participants)
        if self.participant_type == 'watcher':
            mass_mail_watchers(subject, text, participants)
        return self.render_json_response(context)


class LotContentJSON(JSONResponseMixin, LotDetailView):

    def get_files(self, lot):
        def _dict(file):
            return {
                'added': file.added,
                'added_by_name': file.added_by_name,
                'description': file.description,
                'id': file.pk,
                'title': file.title,
                'type': 'file',
                'url': self.request.build_absolute_uri(file.document.url),
            }
        return [_dict(f) for f in lot.files.all()]

    def get_notes(self, lot):
        def _dict(note):
            return {
                'added': note.added,
                'added_by_name': note.added_by_name,
                'id': note.pk,
                'text': note.text,
                'type': 'note',
            }
        return [_dict(n) for n in lot.notes.all()]

    def get_photos(self, lot):
        def _dict(photo):
            return {
                'added': photo.added,
                'added_by_name': photo.added_by_name,
                'description': photo.description,
                'id': photo.pk,
                'name': photo.name,
                'type': 'photo',
                'url': self.request.build_absolute_uri(photo.thumbnail.url),
            }
        return [_dict(p) for p in lot.photos.all()]

    def get_usercontent(self, lot):
        usercontent = self.get_files(lot) + self.get_notes(lot) + self.get_photos(lot)
        usercontent = sorted(usercontent, key=lambda c: c['added'])
        usercontent.reverse()
        return usercontent

    def get(self, request, *args, **kwargs):
        lot = self.object = self.get_object()

        context = {
            'usercontent': self.get_usercontent(lot),
        }

        return self.render_json_response(context)


#
# Autocomplete
#
class LotAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return get_lot_model().objects.none()

        qs = get_lot_model().objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        qs.order_by('name')

        return qs


class LotGroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return get_lotgroup_model().objects.none()

        qs = get_lotgroup_model().objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        qs.order_by('name')

        return qs
