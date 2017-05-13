# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.accounts.api.serializers import ProfileSerializer
from apps.accounts.models import Profile

User = get_user_model()


class OneUserSerializer(serializers.ModelSerializer):
    """
    Class for admin gets, create user

    """

    # In case customer user model might not define a 'username' field,
    # We strive to keep the api DRY, ie. bound to 'username' anyhow.
    # eg. serialized REST response:
    #     {
    #         'profile': {
    #             'age', 33,
    #             'gender', u'F',
    #             'country', u'Guinea'
    #         },
    #         'first_name': u'Therese',
    #         'last_name': u'V',
    #         'mobile_number': u'622422576',
    #         'password': u'luong1234',
    #         'email': u'tvany@techoutlooks.com'
    #     }
    username = serializers.CharField(source='mobile_number', validators=[UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        # fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name',
        #           'is_active', 'date_joined', 'last_login', 'is_admin')
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name',
                  'is_active', 'date_joined', 'last_login', 'is_admin', 'profile')

        read_only_fields = ('date_joined', 'last_login', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User(
    #         **validated_data
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def create(self, validated_data):
        """
        Create a new user with associated profile 
        """
        user_data = validated_data
        profile_data = user_data.pop('profile')

        # create user with password
        # triggers signal that also create an empty profile for this user
        user = User(**user_data)
        user.set_password(validated_data['password'])
        user.save()

        # update profile created by signal
        # with kwargs
        profile = Profile(**profile_data)
        profile.reporter = user
        profile.save()

        return user

    def validate(self, attrs):

        return attrs


class OneUserDetailsSerializer(serializers.ModelSerializer):
    """
    Class for admin get, update and delete user information

    """

    # in case customer user model might not define a 'username' field,
    # let's strive to keep the api DRY, ie. bound to 'username' anyhow.
    username = serializers.CharField(source='mobile_number', validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'date_joined', "last_login", 'is_admin')
        read_only_fields = ('date_joined', 'last_login', 'id')
        extra_kwargs = {'password': {'write_only': True}}


class OneAuthenticatedUserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated user

    """

    # in case customer user model might not define a 'username' field,
    # let's strive to keep the api DRY, ie. bound to 'username' anyhow.
    username = serializers.CharField(source='mobile_number', validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
        read_only_fields = ('date_joined', 'last_login', 'id')


class ChangePasswordUserSerializer(serializers.Serializer):
    """
    Serializer for set password

    """
    #password = serializers.RegexField(min_length=6, max_length=128,
                                      #regex='^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d\~\`\!\@\#\$%\^\&\*\(\)\+\-\_\=\,\;\'\"\[\]\?\<\>\\\.\/\:\{\}\|]{8,}')
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ('password')
        extra_kwargs = {'password': {'write_only': True}}







from collections import OrderedDict

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import flatatt
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _


class RecoverPasswordUserSerializer(serializers.Serializer):
    """
    Serializer for recovering password

    """
    email = serializers.EmailField()

    class Meta:
        fields = ('email')

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.orgs.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='one_accounts/password_reset_subject.txt',
             email_template_name='one_accounts/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             **kwargs):
        """
        A api mimic of django.contrib.auth.forms PasswordResetForm.
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        # perform checks in super
        # instance = super(RecoverPasswordUserSerializer, self).save(**kwargs)

        email = self.validated_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)
        return self.instance
