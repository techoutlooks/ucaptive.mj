# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from dal.autocomplete import Select2QuerySetView
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from queryset_sequence import QuerySetSequence
from .models import CapsMan, Cap, RemoteCap


class CapsManAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = CapsMan.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CapAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Cap.objects.all()
        capsman = self.forwarded.get('capsman', None)
        if capsman:
            qs = qs.filter(capsman=capsman)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CapCoordsAutocomplete(Select2QuerySetSequenceView):
    def get_queryset(self):
        caps = Cap.objects.all()
        remote_caps = RemoteCap.objects.all()

        if self.q:
            caps = caps.filter(capsman__name__contains=self.q)
            remote_caps = remote_caps.filter(capsman__name__contains=self.q)

        # Aggregate querysets
        qs = QuerySetSequence(caps, remote_caps)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(name__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs