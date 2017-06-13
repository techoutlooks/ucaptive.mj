# -*- coding: utf-8 -*-
"""
Views to send email from a contact form.
ContactFormView - for usual form rendering and email sending.
AjaxContactFormView - If the form was submitted using Ajax.

"""
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from ..forms.ureporters import NgLoginForm
# from auth_views import (AjaxableLoginView, LogoutView)

from lib.mixins.views.ajax import AjaxableFormResponseMixin
from lib.mixins.views.context import ExtraContextMixin
from lib.mixins.views.angular import NgFormViewMixin, NgMultipleFormsViewMixin
from lib.mixins.forms.multiforms import MultipleFormsView

import json
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.views.generic import TemplateView, FormView

from ..forms import NgLoginForm, NgUserForm, NgProfileForm


class AuthProvidersPartialView(TemplateView):
    """
        AngularJS controller-bound partial responsible of displaying a list of authentication providers.
        Requires "angular-ui-select" (auth providers rendered in <ui-select></ui-select>).
        Controller: js/accounts/controllers/auth-providers.controller.js
    """
    template_name = 'partials/auth_providers.html'

    def get_context_data(self, **kwargs):
        return {
            'controller': 'AuthProvidersCtrl'
        }


class NgLoginView(NgFormViewMixin, FormView):
    """
    Ajax-able Login view that embeds an AngularJS (unbound) capable Form.
    Does not view however DRF3 API calls however (sent directly to APIView/Serializer).

    """
    template_name = "partials/auth.html"
    form_class = NgLoginForm

    def get_success_url(self):
        return reverse_lazy('layout:home')

    def post(self, request, **kwargs):
        """ Captures Ajax/AngularJS POST. Not DRF3 calls (handled by APIView/Serializer). """

        print "post called"
        if request.is_ajax():
            return self.ajax(request)
        return super(NgLoginView, self).post(request, **kwargs)

    def ajax(self, request):
        print "ajax call"
        form = self.form_class(data=json.loads(request.body))
        response_data = {'errors': form.errors, 'success_url': force_text(self.success_url)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# class UReporterLogoutView(LogoutView):
#     template_name = 'logout.html'
#
#


class NgUserView(NgFormViewMixin, FormView):
    """
    View to send email based on input received from an ajax call.
    Does not view however DRF3 API calls however (sent directly to APIView/Serializer).

    """
    form_class = NgUserForm
    template_name = 'partials/auth.html'

    def get_success_url(self):
        return reverse_lazy('layout:home')

    def post(self, request, **kwargs):
        """ Captures Ajax/AngularJS POST. Not DRF3 calls (handled by APIView/Serializer). """

        if request.is_ajax():
            return self.ajax(request)
        return super(NgUserView, self).post(request, **kwargs)

    def ajax(self, request):
        form = self.form_class(data=json.loads(request.body))
        response_data = {'errors': form.errors, 'success_url': force_text(self.success_url)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class NgProfileView(TemplateView):
    template_name = 'partials/profile.html'


class NgUserRegistrationView(NgMultipleFormsViewMixin, MultipleFormsView):
    """
    Angular View to validate the user and profile forms in a single view.

    """
    form_classes = {
        'user': NgUserForm,
        'profile': NgProfileForm
    }
    scope_prefixes = {
        'user': 'credentials',
        'profile': 'profile'
    }
    form_name = 'registration'
    template_name = 'partials/registration.html'
