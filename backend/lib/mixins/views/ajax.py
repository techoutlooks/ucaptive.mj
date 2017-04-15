# -*- coding: utf-8 -*-
"""
Ajax view mixins library.

"""

import json

from django.core.urlresolvers import resolve
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class AjaxableFormResponseMixin(object):
    """
    A mixin to add AJAX support to a form.
    Must be used with FormView subclasses.
    """
    app_name = None

    def get_app_name(self):
        return self.app_name if hasattr(self, 'app_name') else resolve(self.request.path).app_name

    def get_template_names(self):
        """
        Sets the template name for the view.
        <app_name>/ajax/<template_name> if ajax call else <app_name>/<template_name>
        """

        ajax_path = self.get_app_name() + ('/ajax' if self.request.is_ajax() else '')
        return '{path}/{template}'.format(**{'path': ajax_path, 'template': self.template_name})

    def form_valid(self, form):
        response = super(AjaxableFormResponseMixin, self).form_valid(form)
        form.save()
        messages.success(self.request, _("Your message has been sent successfully."))
        if self.request.is_ajax():
            # success_url unwanted here, we're answering an Ajax call
            # context is returned to the calling script.
            # Consumer of Mixin should override get_context_data()
            context = {}
            return JsonResponse(
                self.get_context_data(context),
            )
        else:
            # Return default implementation
            # Which redirects to success_url
            return response

    def form_invalid(self, form):
        response = super(AjaxableFormResponseMixin, self).form_invalid(form)
        messages.error(self.request, form.errors)
        if self.request.is_ajax():
            return JsonResponse(
                form.errors,
                status=400,
            )
        else:
            # Pop up again the same form
            return self.render_to_response(self.get_context_data(form=form))


