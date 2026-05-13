from django import forms
from django.forms import HiddenInput, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from chosen.forms import ChosenSelectMultiple
from inplace.boundaries.models import Boundary, Layer
from livinglots import get_lot_model, get_owner_model

from .models import Use


class HideLotForm(forms.Form):
    lot = ModelChoiceField(queryset=get_lot_model().objects.all(),
                           widget=HiddenInput())
    use = ModelChoiceField(queryset=Use.objects.filter(visible=False),
                           empty_label=None)


class FiltersForm(forms.Form):

    #
    # Hidden filters
    #
    centroid__within = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    centroid = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    zoom = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    limit = forms.CharField(
        initial='1000',
        required=False,
        widget=forms.HiddenInput,
    )
    parents_only = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput,
    )


    #
    # Default filters
    #
    polygon_area__gt = forms.IntegerField(
        label=_('Area (sq ft) greater than'),
        required=False,
    )
    polygon_area__lt = forms.IntegerField(
        label=_('Area (sq ft) less than'),
        required=False,
    )
    polygon_width__gt = forms.IntegerField(
        label=_('Width (ft) greater than'),
        required=False,
    )
    polygon_width__lt = forms.IntegerField(
        label=_('Width (ft) less than'),
        required=False,
    )
    known_use_certainty__gt = forms.IntegerField(
        initial=3,
        label=_('Known use certainty greater than'),
        required=False,
    )
    known_use_certainty__lt = forms.IntegerField(
        initial=11,
        label=_('Known use certainty less than'),
        required=False,
    )

    participant_types = forms.MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
        ),
        initial=(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    owner__in = forms.ModelMultipleChoiceField(
        label=_('Owner'),
        queryset=get_owner_model().objects.filter(owner_type='public'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    owner__owner_type__in = forms.MultipleChoiceField(
        label=_('Owner types'),
        choices=(
            ('mixed', 'mixed / multiple owners'),
            ('private', 'private'),
            ('public', 'public'),
        ),
        initial=('mixed', 'private', 'public',),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    owner__name__icontains = forms.CharField(
        label=_('Owner name'),
        required=False,
    )

    known_use_existence = forms.MultipleChoiceField(
        choices=(
            ('not in use', _('none')),
            ('in use', _('in use')),
        ),
        initial=('not in use', 'in use',),
        label=_('Known use'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    known_use__name__in = forms.MultipleChoiceField(
        choices=(),
        label=_('Known use category'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['known_use__name__in'].choices = ([('None', 'None'),] +
                                                      self._get_uses())
        for layer in Layer.objects.all():
            self._add_boundary_layer_field(layer)

    def _add_boundary_layer_field(self, layer):
        field_name = 'boundary_%s' % layer.name.replace(' ', '_').lower()
        boundaries = Boundary.objects.order_by_label_numeric(layer=layer)
        self.fields[field_name] = forms.MultipleChoiceField(
            choices=[(b.label, b.label) for b in boundaries],
            initial=(),
            label=_(layer.name),
            widget=ChosenSelectMultiple(attrs={'style': 'width: 100px;',}),
        )

    def _get_uses(self):
        uses = []
        for use in Use.objects.filter(visible=True).order_by('name'):
            uses += [(use.name, use.name),]
        return uses

    def admin_filters(self):
        for field in ('owner__name__icontains',):
            yield self[field]

    def default_filter_names(self):
        return ('polygon_area__gt', 'polygon_area__lt', 'polygon_width__gt',
                'polygon_width__lt', 'known_use_certainty__gt',
                'known_use_certainty__lt',)

    def default_filters(self):
        for field_name in self.default_filter_names():
            yield self[field_name]

    def owners_filters(self):
        for field in ('owner__owner_type__in', 'owner__in',):
            yield self[field]

    def known_use_filters(self):
        for field in ('known_use_existence', 'known_use__name__in',):
            yield self[field]
