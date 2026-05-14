from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from dal import autocomplete
from livinglots import get_lot_model, get_lotgroup_model


class AddToGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=get_lotgroup_model().objects.all().order_by('name'),
        widget=autocomplete.ModelSelect2('lots:lotgroup-autocomplete')
    )

    lots = forms.ModelMultipleChoiceField(
        queryset=get_lot_model().objects.all(),
        widget=forms.MultipleHiddenInput(),
    )


class AddToGroupView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = AddToGroupForm
    permission_required = ('lots.add_lotgroup',)
    template_name = 'admin/lots/lot/add_to_group.html'

    def get_context_data(self, **kwargs):
        context = super(AddToGroupView, self).get_context_data(**kwargs)
        context.update({
            'is_popup': False,
            'opts': get_lotgroup_model()._meta,
            'title': _('Add Lots to Group'),
            'lots': get_lot_model().objects.filter(
                pk__in=self.request.GET.get('ids', '').split(','),
            ).order_by('address_line1'),
        })
        return context

    def get_initial(self):
        initial = super(AddToGroupView, self).get_initial()
        initial.update({
            'lots': get_lot_model().objects.filter(
                pk__in=self.request.GET.get('ids', '').split(','),
            ),
        })
        return initial

    def get_success_url(self):
        return reverse('admin:lots_lot_changelist')

    def form_valid(self, form):
        group = form.cleaned_data['group']
        lots = form.cleaned_data['lots']
        lots_added_to_group = lots.count()

        self._add_to_group(group, lots)

        messages.success(self.request, ('Added %d lots to %s' %
                                        (lots_added_to_group, group.name)))
        return super(AddToGroupView, self).form_valid(form)

    def _add_to_group(self, group, lots):
        """Add lots to a group."""
        for lot in lots:
            lot.group = group
            lot.save()
