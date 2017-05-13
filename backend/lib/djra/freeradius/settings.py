# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
__author__ = 'ceduth'


def get_setting(name):
    from django.conf import settings
    from django.utils.translation import ugettext_lazy as _

    DEFAULT_GROUPS = ('default',)
    DEFAULT_PASSWORD_ATTRIBUTE = 'Cleartext-Password'
    DEFAULT_PASSWORD = ''                                   # If user is imported from xls

    default = {
        'DJRA_DEFAULT_GROUPS': getattr(settings, 'DJRA_DEFAULT_GROUPS', DEFAULT_GROUPS),
        'DJRA_DEFAULT_PASSWORD_ATTRIBUTE': getattr(settings, 'DJRA_DEFAULT_PASSWORD_ATTRIBUTE', DEFAULT_PASSWORD_ATTRIBUTE),
        'DJRA_DEFAULT_PASSWORD': getattr(settings, 'DJRA_DEFAULT_PASSWORD', DEFAULT_PASSWORD),

    }
    return default['DJRA_%s' % name]