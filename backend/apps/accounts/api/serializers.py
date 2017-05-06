# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from rest_framework import serializers
from ..models import Reporter, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('age', 'gender', 'country', 'region', 'city')


class ReporterSerializer(serializers.ModelSerializer):
    """
    Serialize/Deserialize a U-Reporter object.

    """
    profile = ProfileSerializer(required=True)

    class Meta:
        model = Reporter
        fields = (
            'id', 'last_login', 'is_superuser', 'email', 'first_name', 'last_name', 'date_joined', 'is_active',
            'is_admin', 'mobile_number', 'profile'
        )
        read_only_fields = ('id', 'last_login', 'date_joined')

    def create(self, validated_data):

        # create user
        user_data = {}
        user_fields = self.Meta.fields
        for f in user_fields:
            user_data.update({f:validated_data.get(f)})
        print "*** user_data %s ***" % user_data
        reporter = Reporter(**user_data)
        reporter.set_password(validated_data['password'])

        # assign profile
        profile_data = {}
        profile_fields = ProfileSerializer.Meta.fields
        for f in profile_fields:
            profile_data.update({f:validated_data.get(f)})
        print "*** profile_data %s ***" % profile_data
        profile = Profile(**profile_data)

        # save user (and profile via signal)
        reporter.profile = profile
        reporter.save()
        return reporter

    # def update(self, instance, validated_data):
    #     assert instance.username == validated_data['username']
    #     instance.update(password=validated_data['password'],
    #                    is_active=validated_data['is_active'],
    #                    groups=validated_data['groups'].split(','))
    #     instance.save()
    #     return instance