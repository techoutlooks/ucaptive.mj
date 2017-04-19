# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.http import HttpResponse

from tastypie.api import Api

# from djra.freeradius.api import RadUserResource, RadGroupResource

admin.autodiscover()

# curl http://localhost:8000/api/djra/v1/
# v1_api = Api(api_name='v1')
# v1_api.register(RadUserResource())
# v1_api.register(RadGroupResource())


def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')


i18n_urls = [
    url(r'^', include('layout.urls', namespace='layout')),
    url(r'^radmin/', include('djra.radmin.urls')),
    url(r'^reports/', include('djra.reports.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),          # chained models (smart_select) in user profile
]

urlpatterns = [
    url(r'^robots\.txt$', render_robots),
    url(r'^djra/', include('djra.freeradius.urls')),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
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
