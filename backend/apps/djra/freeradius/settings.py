# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def get_setting(name):
    from django.conf import settings
    from django.utils.translation import ugettext_lazy as _

    DJRA_DEFAULT_GROUP = 'default'

    default = {
        'DJRA_DEFAULT_GROUP': getattr(settings, 'DJRA_DEFAULT_GROUP', DJRA_DEFAULT_GROUP),

    }
    return default['DJRA_%s' % name]