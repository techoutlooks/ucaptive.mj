#-*- coding: utf-8 -*-

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse # python3 support
from .utils import default_redirect
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormView
from django.conf import settings

from django.core.urlresolvers import resolve
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class AjaxableLoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.

    Usage:
        in views.py:
            url(r'^login/$',
                LoginView.as_view(
                    form_class=MyCustomAuthFormClass,
                    success_url='/my/custom/success/url/),
                name="login"),

    """
    form_class = AuthenticationForm
    template_name = 'login.html'                    # default template
    redirect_field_name = REDIRECT_FIELD_NAME

    # custom
    app_name = None
    extra_context = {'success':_("Your account were successfully created.")}

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(AjaxableLoginView, self).dispatch(*args, **kwargs)

    def get_app_name(self):
        return self.app_name if hasattr(self, 'app_name') else resolve(self.request.path).app_name

    def get_template_names(self):
        ajax_path = self.get_app_name() + ('/ajax' if self.request.is_ajax() else '')
        return '{path}/{template}'.format(**{'path': ajax_path, 'template': self.template_name})

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())

        response = super(AjaxableLoginView, self).form_valid(form)
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
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()

        super(AjaxableLoginView, self).form_invalid(form)
        messages.error(self.request, form.errors)
        if self.request.is_ajax():
            return JsonResponse(
                form.errors,
                status=400,
            )
        else:
            # Pop up again the same form
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, ''))

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(AjaxableLoginView, self).get(request, *args, **kwargs)


class LogoutView(TemplateResponseMixin, View):
    template_name = "logout.html"
    redirect_field_name = "next"

    # custom
    app_name = None

    def get_app_name(self):
        return self.app_name if hasattr(self, 'app_name') else resolve(self.request.path).app_name

    def get_template_names(self):
        ajax_path = self.get_app_name() + ('/ajax' if self.request.is_ajax() else '')
        return '{path}/{template}'.format(**{'path': ajax_path, 'template': self.template_name})

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()

        if self.request.is_ajax():
            return JsonResponse(
                context,
            )

        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        redirect_field_value = self.request.POST.get(
            redirect_field_name, self.request.GET.get(redirect_field_name, ''))
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
            })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

