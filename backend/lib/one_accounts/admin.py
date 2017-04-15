from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
if admin.site.is_registered(Group):
    admin.site.unregister(Group)
admin.site.register(User)
