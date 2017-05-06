# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def get_setting(name):
    from django.conf import settings
    from django.utils.translation import ugettext_lazy as _

    DEFAULT_GROUP = 'default'
    DEFAULT_PASSWORD_ATTRIBUTE = 'Cleartext-Password'

    default = {
        'DJRA_DEFAULT_GROUP': getattr(settings, 'DJRA_DEFAULT_GROUP', DEFAULT_GROUP),
        'DJRA_DEFAULT_PASSWORD_ATTRIBUTE': getattr(settings, 'DJRA_DEFAULT_PASSWORD_ATTRIBUTE', DEFAULT_PASSWORD_ATTRIBUTE),

    }
    return default['DJRA_%s' % name]