# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from rest_framework import viewsets, mixins, filters, status
from rest_condition import Or, Not

from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework_api_key.authentication import ApiKeyAuthentication

from ..models import Reporter
from .serializers import ReporterSerializer


class ReporterApi(viewsets.ModelViewSet):
    """
    DRF3 ViewSet for admin CRUD operations on U-Reporters.
    Requires a valid API key. No login required.

    GET, POST   /accounts/api/v1/
    PUT, DELETE /accounts/api/v1/caps/{radio_mac|base_mac}/$

    """
    serializer_class = ReporterSerializer
    authentication_classes = (ApiKeyAuthentication,)
    permission_classes = (HasAPIAccess,)
    # lookup_field = lookup_url_kwarg = 'mobile_number'

    def get_queryset(self):
        return Reporter.objects.all()
