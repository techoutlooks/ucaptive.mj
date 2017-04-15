from __future__ import unicode_literals
from django.db import models
from . import crypto
from .settings import oneauth_settings
from django.conf import settings
from django.utils import timezone


class OneAuthTokenManager(models.Manager):
    def create(self, user, expires=oneauth_settings.TOKEN_TTL):
        token = crypto.create_token_string()
        salt = crypto.create_salt_string()
        digest = crypto.hash_token(token, salt)

        if expires is not None:
            expires = timezone.now() + expires

        super(OneAuthTokenManager, self).create(digest=digest, salt=salt, user=user, expires=expires)
        return token  # Note only the token - not the AuthToken object - is returned


class OneAuthToken(models.Model):
    objects = OneAuthTokenManager()

    digest = models.CharField(max_length=oneauth_settings.DIGEST_LENGTH, primary_key=True)
    salt = models.CharField(max_length=oneauth_settings.SALT_LENGTH, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name="auth_token_set")
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "one_authentication"

    def __str__(self):
        return "%s : %s" % (self.digest, self.user)
