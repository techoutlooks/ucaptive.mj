# -*- coding: utf-8 -*-
__author__ = 'TOANTV'
from django.utils import timezone
from .models import OneAuthToken
from .crypto import hash_token
from rest_framework import authentication
from rest_framework import exceptions


class OneTokenAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_ONE_TOKEN')
        if not token:
            return None
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """
        Due to the random nature of hashing a salted value, this must inspect
        each auth_token individually to find the correct one.
        Tokens that have expired will be deleted and skipped
        """
        for auth_token in OneAuthToken.objects.all():
            if auth_token.expires is not None:
                if auth_token.expires < timezone.now():
                    auth_token.delete()
                    continue
            try:
                digest = hash_token(token, auth_token.salt)
            except Exception:
                raise exceptions.AuthenticationFailed('Token is invalid.')

            if digest == auth_token.digest:
                return self.validate_user(auth_token)
        # Authentication with this token has failed
        raise exceptions.AuthenticationFailed('Token is invalid.')

    def validate_user(self, auth_token):
        if not auth_token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        return (auth_token.user, auth_token)

    def delete_another_tokens(self, user):
        one_auth_tokens = OneAuthToken.objects.filter(user=user)
        for auth_tokens in one_auth_tokens:
            auth_tokens.delete()
