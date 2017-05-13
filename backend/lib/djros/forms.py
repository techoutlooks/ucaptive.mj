# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm
from .helpers import booleanify
from .models import Cap, RemoteCap, CapCoords

from queryset_sequence import QuerySetSequence
from dal.autocomplete import ModelSelect2, FutureModelForm
from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2
from dal_queryset_sequence.fields import QuerySetSequenceModelField


class CapForm(ModelForm):
    class Meta:
        model = Cap
        fields = '__all__'

        # dal aka. autocomplete_light
        widgets = {
            'capsman': ModelSelect2(
                url='capsman-autocomplete',
                forward=['capsman'],
                attrs={'data-placeholder': _("Owning CAPsMAN ?"), }
            ),
        }

    def clean_disabled(self):
        return booleanify(self.cleaned_data.get('disabled'))

    def clean_running(self):
        return booleanify(self.cleaned_data.get('running'))

    def clean_inactive(self):
        return booleanify(self.cleaned_data.get('inactive'))

    def clean_bound(self):
        return booleanify(self.cleaned_data.get('bound'))


class CapCoordsForm(FutureModelForm):
    cap = QuerySetSequenceModelField(
        queryset=QuerySetSequence(
            Cap.objects.all(),
            RemoteCap.objects.all(),
        ),
        required=False,
        widget=QuerySetSequenceSelect2('cap-autocomplete'),
    )

    class Meta:
        model = CapCoords
        fields = '__all__'
