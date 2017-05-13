# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from .models import Profile


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(reporter=instance)
    instance.profile.save()


def run_clean(sender, instance, **kwargs):
    instance.clean()
