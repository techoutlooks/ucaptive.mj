from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FreeRadiusConfig(AppConfig):
    name = 'djra.freeradius'
    verbose_name = _('FreeRadius 3.0')

    def ready(self):
        from . import signals  # noqa
