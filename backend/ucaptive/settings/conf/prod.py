from os.path import join

from .staging import Staging
from lib.settings.conf import ProdSettingsMixin
from lib.settings.mixins import EmailMixin


class Prod(EmailMixin, ProdSettingsMixin, Staging):
    """ Production settings with email logging. """
    pass
