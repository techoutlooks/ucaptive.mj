# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from . import views

# Views post-processed in AngularJS
# controller, must match value define in ng's ui-router provider.

ng_urlpatterns = [
    # url(r'^auth_providers/$', views.AuthProvidersPartialView.as_view(), name='ng-auth-providers'),
    url(r'^signin/$', views.NgLoginView.as_view(scope_prefix='credentials'), name='ng-login'),
    url(r'^register/$', views.NgRegistrationView.as_view(scope_prefix='credentials'), name='ng-register'),
    url(r'^profile/$', views.NgProfileView.as_view(), name='ng-profile'),
]

# Restful api

urlpatterns = [
    # # auth_cbv
    # url(r'^login/$', views.UReporterLoginView.as_view(app_name='one_accounts'), name='one_accounts-login'),
    # url(r'^logout/$', views.UReporterLogoutView.as_view(app_name='one_accounts'), name='one_accounts-logout'),

    # # django-registration
    # url(r'^', include('registration.backends.simple.urls')),
    # url(r'^import/$', views.UReportDataImporterCreateView.as_view(), name='import-ureporters'),

    url(r'^', include(ng_urlpatterns)),

    # Restful Views
    # url(r'^api/v1/$', api.UserListCreate.as_view(), name='ng-users-listcreate'),
    url(r'^api/v1/', include('one_accounts.urls'))
]
