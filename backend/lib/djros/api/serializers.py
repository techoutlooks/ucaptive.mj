# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from rest_framework import serializers
from ..models import Cap, Radio


class CapSerializer(serializers.ModelSerializer):
    """
    Class for admin gets, create user

    """

    # has to match FormView @radmin.views.UserDetailView, or
    # todo: let serializer display the angular radmin.forms.RadUserForm intially?

    class Meta:
        model = Cap
        fields = ('name', 'radio_mac', 'bound', 'running', 'inactive', 'disabled', 'current_channel')
        read_only_fields = fields   # as of now


class RadioSerializer(serializers.ModelSerializer):
    """
    Class for admin gets, create user

    """

    # has to match FormView @radmin.views.UserDetailView, or
    # todo: let serializer display the angular radmin.forms.RadUserForm intially?

    class Meta:
        model = Radio
        fields = ('interface', 'mac_address') #, 'rx_signal', 'bytes', 'tx_rate', 'rx_rate', 'tx_rate_set', 'uptime')
        read_only_fields = fields   # read-only model
