# -*- coding: utf-8 -*-

from lib.settings.conf import DevSettingsMixin
from .base import Base


class Dev(DevSettingsMixin, Base):
    pass


