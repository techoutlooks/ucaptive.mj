# -*- coding: utf-8 -*-

import random
import string
import itertools

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, filters, status
from rest_framework import serializers

from lib.restutils import JSONResponse
from one_auth.authentication import OneTokenAuthentication
from one_accounts.permissions import IsOneSuperAdmin

from ..models import RadUser, Radgroupcheck, RadGroup
from .serializers import RadUserSerializer, RadGroupSerializer


User = get_user_model()


class RadUserApi(viewsets.ModelViewSet):
    """
    DRF3 ViewSet for CRUD operations on Freeradius v3.0 users
    
    GET, POST   /api/v1/radusers/
    PUT, DELETE /api/v1/radusers/{username}/$
    
    """
    serializer_class = RadUserSerializer
    permission_classes = [IsOneSuperAdmin]
    authentication_classes = (OneTokenAuthentication,)
    lookup_field = lookup_url_kwarg = 'username'
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ['username', 'password', 'is_active', 'is_online', 'groups']

    def get_queryset(self):
        return RadUser.objects.all()
        # don't list up admins
        admins = [u.get_username() for u in User.objects.filter(is_admin=True)]
        return RadUser.objects.exclude(username__in=admins)


class RadGroupApi(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    DRF3 ViewSet for CRUD operations on Freeradius v3.0 groups
    
    GET, POST   /api/v1/radgroups/
    PUT, DELETE /api/v1/radgroups/{username}/$
    
    """
    serializer_class = RadGroupSerializer
    permission_classes = [IsOneSuperAdmin]
    authentication_classes = (OneTokenAuthentication,)
    # lookup_url_kwarg = 'username'
    #
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('username', 'is_active', 'is_admin')

    def get_queryset(self):
        radgc_records = Radgroupcheck.objects.all().order_by('groupname')
        groups = []
        for g, rows in itertools.groupby(radgc_records, lambda x: x.groupname):
            groups.append(self._build_group(g, list(rows)))
        return groups

    def get_object(self):
        groupname = self.kwargs.get('pk')
        radgc_records = Radgroupcheck.objects.filter(groupname=groupname)
        if len(radgc_records) == 0:
            return JSONResponse({'status': 'Radius Group not found.'}, status=status.HTTP_404_NOT_FOUND)

        return self._build_group(groupname, radgc_records)

    def _build_group(self, groupname, radgc_records):
        attrs = []
        for radgc in radgc_records:
            attrs.append({'attribute' : radgc.attribute,
                            'op' : radgc.op,
                            'value' : radgc.value})
        return RadGroup(groupname, attrs)

