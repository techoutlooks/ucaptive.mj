# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
__author__ = 'ceduth'


from configurations import values
from .constants import *


# Mikrotik commands
# used internally

CAPSMAN_DEFAULT_SYNC_TYPE = CAPSMAN_CAP_TYPE_INTERFACE          # We sync from cmd '/caps-man/remote-cap' by default


# Django settings
# exposed thru django.conf.settings


def get_setting(name):
    from django.conf import settings
    from .models import Cap, RemoteCap

    ############################################
    # RouterOS connection settings
    CAPSMAN_DEFAULT_IP = ROUTEROS_DEFAULT_IP = '192.168.0.2'    # by defaut,
    CAPSMAN_DEFAULT_LOGIN = ROUTEROS_DEFAULT_LOGIN = 'admin'    # set identically for all CAPsMANs
    CAPSMAN_DEFAULT_PASSWORD = ROUTEROS_DEFAULT_PASSWORD = ''   # managed by DjROS

    ############################################
    # caps

    CAPSMAN_CAP_TYPES = {
        # Cap and RemoteCap types
        # as respectivrly listed by above Mikrotik commands.
        CAPSMAN_CAP_TYPE_REMOTE: {
            'model': RemoteCap,
            'cmd': CAPSMAN_GET_REMOTE_CAPS_CMD,
            'model_lookup_field': CAPSMAN_REMOTE_CAP_LOOKUP_FIELD
        },
        CAPSMAN_CAP_TYPE_INTERFACE: {
            'cmd': CAPSMAN_GET_CAPS_INTERFACES_CMD,
            'model': Cap,
            'model_lookup_field': CAPSMAN_CAP_INTERFACES_LOOKUP_FIELD
        }
    }

    default = {
        'DJROS_ROUTEROS_DEFAULT_IP': getattr(settings, 'DJROS_ROUTEROS_DEFAULT_IP', ROUTEROS_DEFAULT_IP),
        'DJROS_ROUTEROS_DEFAULT_LOGIN': getattr(settings, 'DJROS_ROUTEROS_DEFAULT_LOGIN', ROUTEROS_DEFAULT_LOGIN),
        'DJROS_ROUTEROS_DEFAULT_PASSWORD': getattr(settings, 'DJROS_ROUTEROS_DEFAULT_PASSWORD',
                                                   ROUTEROS_DEFAULT_PASSWORD),

        'DJROS_CAPSMAN_DEFAULT_IP': CAPSMAN_DEFAULT_IP,
        'DJROS_CAPSMAN_DEFAULT_LOGIN': CAPSMAN_DEFAULT_LOGIN,
        'DJROS_CAPSMAN_DEFAULT_PASSWORD': CAPSMAN_DEFAULT_PASSWORD,
        'DJROS_CAPSMAN_REMOTE_CAP_LOOKUP_FIELD': getattr(settings, 'DJROS_CAPSMAN_REMOTE_CAP_LOOKUP_FIELD',
                                                         CAPSMAN_REMOTE_CAP_LOOKUP_FIELD),
        'DJROS_CAPSMAN_CAP_INTERFACES_LOOKUP_FIELD': getattr(settings, 'DJROS_CAPSMAN_CAP_INTERFACES_LOOKUP_FIELD',
                                                             CAPSMAN_CAP_INTERFACES_LOOKUP_FIELD),
        'DJROS_CAPSMAN_CAP_TYPES': getattr(settings, 'DJROS_CAPSMAN_CAP_TYPES', CAPSMAN_CAP_TYPES),
        'DJROS_CAPSMAN_SYNC_ENABLED_CAPS_ONLY': getattr(settings, 'DJROS_CAPSMAN_SYNC_ENABLED_CAPS_ONLY', False),
        'DJROS_CAPSMAN_DEFAULT_SYNC_TYPE': getattr(settings, 'DJROS_CAPSMAN_DEFAULT_SYNC_TYPE', CAPSMAN_DEFAULT_SYNC_TYPE),

        'DJROS_CAPSMAN_RADIOS_LOOKUP_FIELD': getattr(settings, 'DJROS_CAPSMAN_RADIOS_LOOKUP_FIELD', CAPSMAN_RADIOS_LOOKUP_FIELD),
        'DJROS_CAPSMAN_RADIOS_CAP_PTR_FIELD': getattr(settings, 'DJROS_CAPSMAN_RADIOS_CAP_PTR_FIELD', CAPSMAN_RADIOS_CAP_PTR_FIELD),

    }
    return default['DJROS_%s' % name]


class DjROSSettingsMixin(object):
    """
    Django settings for DJROS.
     
    """

    # TODO: RouterOS settings

    # Default CAPsMAN settings to fallback to,
    # if none found from model (Cf. djros.models.CapsMan)
    DJROS_CAPSMAN_DEFAULT_IP = values.IPValue(environ_prefix='')
    DJROS_CAPSMAN_DEFAULT_LOGIN = values.Value(environ_prefix='')
    DJROS_CAPSMAN_DEFAULT_PASSWORD = values.SecretValue(environ_prefix='')

    # For geo-locating CAPs
    GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyDD85eI1-uiNlsFDnsdh3t7dP0sNjTW2c4' # same throughout project (accounts.constants.js)
    MAP_WIDGET_HEIGHT = 500
    GEOPOSITION_MAP_OPTIONS = {
        'minZoom': 3,
        'maxZoom': 15,
        'ceter': {'lat': 52.5, 'lng': 13.4}
    }

    @property
    def DEFAULT_APPS(self):
        """ Add self and CAPs locator aka. django-geoposition """
        existing_apps = super(DjROSSettingsMixin, self).DEFAULT_APPS
        djros_apps = ('geoposition', 'djros', 'queryset_sequence',)
        return self.add_apps(djros_apps, existing_apps)

    @property
    def ADMIN_APPS(self):
        """ Nest CAPs as NestedGenericTabularInline under CAPsMAN in django admin. """
        existing_apps = super(DjROSSettingsMixin, self).ADMIN_APPS
        djros_apps = ('dal', 'dal_select2', 'dal_queryset_sequence')
        return self.add_apps(djros_apps, existing_apps)

    # Grappelli admin theme
    # settings.DEFAULT_APPS += ('grappelli',) already
    GRAPPELLI_ADMIN_TITLE = 'uCaptive MJ v1.0 (Staff Only)'
