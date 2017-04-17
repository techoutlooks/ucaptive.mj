# -*- coding: utf-8 -*-

from os.path import join

from .dev import Dev
from lib.settings.conf import StagingSettingsMixin


class Staging(StagingSettingsMixin, Dev):
    """ Testing before going production """
    pass

    #todo: debugging only, move to env
    WWW_DIR = '/var/www/html/apps/ucaptive.mj'
    LOGGING_DIR = '/srv/log/apps/ucaptive.mj/'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    #endofdeleteme