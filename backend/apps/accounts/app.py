from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.utils.translation import ugettext_lazy as _

from .signals import create_or_update_user_profile, run_clean


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = _('This Project\'s Users')

    def ready(self):
        User = get_user_model() # Reporter
        # post_save.connect(create_or_update_user_profile, sender=User)

        # clean User model fields before saving
        pre_save.connect(run_clean, sender=User)
