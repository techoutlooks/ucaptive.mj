# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from lib.mixins.views.context import ExtraContextMixin
from lib.utils.format import srandom


class OnePageAppView(TemplateView):
    template_name = "index.html"


class HomePartialView(ExtraContextMixin, TemplateView):
    template_name = "partials/home.html"
    extra_context = {
        'carousel': {
            'controller': 'CarouselCtrl'
        }
    }


class AboutPartialView(TemplateView):
    template_name = "partials/about.html"


class MapsPartialView(TemplateView):
    template_name = "partials/maps.html"


class NewsPartialView(TemplateView):
    template_name = "partials/news.html"


class ServicesPartialView(TemplateView):
    template_name = "partials/services.html"


class ProjectsPartialView(TemplateView):
    template_name = "partials/projects.html"


class NgModalView(ExtraContextMixin, TemplateView):
    """
        AngularJS UI Bootstrap view that displays a modal window.
        The template is used as override for windowTemplateUrl

        Cf. Modal (ui.bootstrap.modal) at http://angular-ui.github.io/bootstrap/

    """
    template_name = 'partials/modal.html'
