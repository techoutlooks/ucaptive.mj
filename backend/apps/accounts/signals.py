
from .models import Profile


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(reporter=instance)
    instance.profile.save()
