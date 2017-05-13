# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.conf.urls import patterns, include, url
from apps.accounts import views


# Views post-processed in AngularJS
# controller, must match value define in ng's ui-router provider.

ng_urlpatterns = [
    # url(r'^auth_providers/$', views.AuthProvidersPartialView.as_view(), name='ng-auth-providers'),
    url(r'^signin/$', views.NgLoginView.as_view(scope_prefix='credentials'), name='ng-login'),
    # url(r'^register/$', views.NgUserView.as_view(scope_prefix='credentials'), name='ng-register'),
    url(r'^register/$', views.NgUserRegistrationView.as_view(), name='ng-register'),
    url(r'^profile/$', views.NgProfileView.as_view(), name='ng-profile'),
]

dj_urlpatterns = [
    # TODO: regular django views. To angular?
    # # auth_cbv
    # url(r'^login/$', views.UReporterLoginView.as_view(app_name='one_accounts'), name='one_accounts-login'),
    # url(r'^logout/$', views.UReporterLogoutView.as_view(app_name='one_accounts'), name='one_accounts-logout'),

    # # django-registration
    # url(r'^', include('registration.backends.simple.urls')),
    url(r'^import/$', views.UReportDataImporterCreateView.as_view(), name='import-ureporters'),
]

urlpatterns = [
    url(r'^', include(ng_urlpatterns)),
    url(r'^', include(dj_urlpatterns)),
]



