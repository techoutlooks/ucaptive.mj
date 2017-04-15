# -*- coding: utf-8 -*-
"""
Semi-generic views that can be used directly in the URLSconf
and pass extra_context dict to the as_view() call; e.g.:

url(r'^camera/(?P<pk>\d+)/$',
    views.ExtraDetailView.as_view(model=models.Camera,
                                  extra_context={'action_type': 'detail', 'mod_name' : 'camera'},
                                  template_name='cameras/camera_detail.html'),
                                  name='camera_detail'),
"""
from django.views import generic


class ExtraContextMixin(object):
    extra_context = {}

    def get_context_data(self, context=None, **kwargs):
        # don't pull existing context if called with custom context
        if context is None:
            context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ExtraListView(ExtraContextMixin, generic.ListView):
    pass


class ExtraDetailView(ExtraContextMixin, generic.DetailView):
    pass


class ExtraUpdateView(ExtraContextMixin, generic.UpdateView):
    pass


class ExtraCreateView(ExtraContextMixin, generic.CreateView):
    pass


class ExtraDeleteView(ExtraContextMixin, generic.DeleteView):
    pass


class ExtraCloneView(ExtraUpdateView):
    def post(self, request, *args, **kwargs):
        return ExtraCreateView.as_view(model=self.model,
                                       template_name=self.template_name,
                                       extra_context=self.extra_context)(request, *args, **kwargs)
