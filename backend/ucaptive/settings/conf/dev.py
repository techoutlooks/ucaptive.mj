# -*- coding: utf-8 -*-

from lib.settings.conf import DevSettingsMixin
from .base import BaseSettings


class Dev(DevSettingsMixin, BaseSettings):
    pass


