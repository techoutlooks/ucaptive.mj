# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from rest_framework import serializers
from ..models import RadUser, RadGroup
from ..settings import get_setting


class RadUserSerializer(serializers.ModelSerializer):
    """
    Class for admin gets, create user

    """

    # has to match FormView @radmin.views.UserDetailView, or
    # todo: let serializer display the angular radmin.forms.RadUserForm intially?
    password = serializers.CharField()
    is_active = serializers.BooleanField(required=False)
    groups = serializers.CharField(required=False)

    class Meta:
        model = RadUser
        fields = ('id', 'username', 'password', 'is_active', 'groups')
        read_only_fields = ('is_online', 'id')
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_groups = validated_data.get('groups')
        groups = validated_groups.split(',') if validated_groups else get_setting('DEFAULT_GROUPS')
        validated_data.update({'groups': groups})

        # we must .create() to update op, value attrs
        return RadUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        assert instance.username == validated_data['username']
        instance.update(password=validated_data['password'],
                       is_active=validated_data['is_active'],
                       groups=validated_data['groups'].split(','))
        instance.save()
        return instance


class RadGroupSerializer(serializers.ModelSerializer):
    """
    Class for admin gets, create user

    """

    # in case customer user model might not define a 'username' field,
    # let's strive to keep the api DRY, ie. bound to 'username' anyhow.
    # username = serializers.CharField(source='mobile_number')

    class Meta:
        model = RadUser
        fields = ('id', 'username', 'is_active', 'groups')
        read_only_fields = ('is_online', 'id')
        extra_kwargs = {'password': {'write_only': True}}
