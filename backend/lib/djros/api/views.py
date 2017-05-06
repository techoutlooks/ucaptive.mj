# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from rest_framework import viewsets, mixins, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_condition import Or, Not

from one_auth.authentication import OneTokenAuthentication
from one_accounts.api.permissions import IsAdminOrReadOnly

from ..models import Cap, Radio
from .serializers import CapSerializer, RadioSerializer
from .parsers import HyphenJSONParser
from .. settings import get_setting


# FIXME: set permission_classes, authentication_classes to ApiKey*

class CapApi(viewsets.ModelViewSet):
    """
    DRF3 ViewSet for CRUD operations on Freeradius v3.0 users

    GET, POST   /djros/api/v1/caps/
    PUT, DELETE /djros/api/v1/caps/{radio_mac|base_mac}/$

    """
    serializer_class = CapSerializer
    parser_classes = (HyphenJSONParser,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (OneTokenAuthentication,)

    # auto guess lookup field from settings
    lookup_field = lookup_url_kwarg = get_setting('CAPSMAN_CAP_TYPES')[
        get_setting('CAPSMAN_DEFAULT_SYNC_TYPE')]['model_lookup_field']

    def get_queryset(self):
        return Cap.objects.all()


class RadioApi(viewsets.ModelViewSet):
    """
    DRF3 ViewSet for CRUD operations on Freeradius v3.0 users

    GET, POST   /djros/api/v1/caps/
    PUT, DELETE /djros/api/v1/caps/{radio_mac|base_mac}/$

    """
    serializer_class = RadioSerializer
    parser_classes = (HyphenJSONParser,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (OneTokenAuthentication,)

    # auto guess lookup field from settings
    lookup_field = lookup_url_kwarg = get_setting('CAPSMAN_RADIOS_LOOKUP_FIELD')

    def get_queryset(self):
        return Radio.objects.all()