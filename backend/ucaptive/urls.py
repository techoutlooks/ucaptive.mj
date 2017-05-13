# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
__author__ = 'ceduth'


from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()


# FIXME: Refactor/Delete Tastypie after testing replacement by DRF3.
# from tastypie.api import Api
# from djra.freeradius.api import RadUserResource, RadGroupResource

# curl http://localhost:8000/api/djra/v1/
# v1_api = Api(api_name='v1')
# v1_api.register(RadUserResource())
# v1_api.register(RadGroupResource())


def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')


i18n_urls = [
    url(r'^', include('apps.layout.urls', namespace='layout')),
    url(r'^accounts/', include('apps.accounts.urls.views')),
    url(r'^radmin/', include('djra.radmin.urls')),
    url(r'^reports/', include('djra.reports.urls')),

    url(r'^cities/', include('apps.cities.urls', namespace='cities')),
    # url(r'^chaining/', include('smart_selects.urls')),          # chained models (smart_select) in user profile

    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

api_urls = [
    url(r'^djra/api/v1/', include('djra.freeradius.urls')),
    url(r'^djros/api/v1/', include('djros.urls')),
    url(r'^accounts/api/v1/users/', include('one_accounts.urls')),
    url(r'^accounts/api/v1/', include('apps.accounts.urls.api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^autocomplete/', include('autocomplete_light.urls')),
    # url(r'^cities/api/v1/', include('cities_light.contrib.restframework3')),
]

urlpatterns = [
    url(r'^robots\.txt$', render_robots),
    url(r'^', include(api_urls)),
]


if settings.USE_I18N:
    urlpatterns += i18n_patterns('', *i18n_urls)
else:
    urlpatterns += i18n_urls


if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
