from os.path import join

from .staging import Staging
from lib.settings.conf import ProdSettingsMixin
from lib.settings.mixins import SendMailMixin


class Prod(SendMailMixin, ProdSettingsMixin, Staging):
    """ Production settings with email logging. """
    pass
