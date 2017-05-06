# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.conf.urls import url, include
from rest_framework import routers
from . import api


# DjROS v1.0 API

router = routers.SimpleRouter()
router.register(r'caps', api.CapApi, base_name='cap')
router.register(r'radios', api.RadioApi, base_name='radio')


urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]