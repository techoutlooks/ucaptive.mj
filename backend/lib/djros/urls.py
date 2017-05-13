# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.conf.urls import url, include
from rest_framework import routers
from . import api
from .views import CapsManAutocomplete, CapAutocomplete, CapCoordsAutocomplete


# DjROS v1.0 API
router = routers.SimpleRouter()
router.register(r'caps', api.CapApi, base_name='cap')
router.register(r'radios', api.RadioApi, base_name='radio')
api_patterns = [
    url(r'^', include(router.urls, namespace='api')),
]

# DAL v3
dal_patterns = [
    url( r'^cap-coords-autocomplete/$', CapCoordsAutocomplete.as_view(), name='cap-autocomplete'),
    url(r'^cap-autocomplete/$', CapAutocomplete.as_view(), name='cap-autocomplete'),
    url(r'^capsman-autocomplete/$', CapsManAutocomplete.as_view(), name='capsman-autocomplete'),

]

urlpatterns = api_patterns + dal_patterns

