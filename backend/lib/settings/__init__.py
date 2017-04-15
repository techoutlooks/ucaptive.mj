# settings/__init__.py
from __future__ import unicode_literals

import os
import sys
import socket
import environ # django-environ
import logging.config
from os.path import exists, join, dirname, abspath, pardir

from configurations import Configuration, values
from split_settings.tools import optional, include

from .mixins import *
_ = lambda x: x


# Split our configurations
# https://django-environ.readthedocs.org/en/latest/
# https://github.com/sobolevn/django-split-settings
include(
    'config/base.py',
    'config/dev.py',
    'config/staging.py',
    'config/prod.py',

    # Eventual host-specific python code !
    optional('config/%s.py' % socket.gethostname().split('.', 1)[0]),

    scope=globals()
)
