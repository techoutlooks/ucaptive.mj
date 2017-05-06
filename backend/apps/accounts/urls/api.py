# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.conf.urls import patterns, include, url
from rest_framework import routers
from apps.accounts import api


# U-Reporters API,

router = routers.SimpleRouter()
router.register(r'', api.ReporterApi, base_name='accounts')

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]