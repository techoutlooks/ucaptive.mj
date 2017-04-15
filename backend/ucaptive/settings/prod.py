from os.path import join

from .staging import Staging
from lib.settings import ProdSettingsMixin,EmailMixin


class Prod(EmailMixin, ProdSettingsMixin, Staging):
    """ Production settings with email logging. """
    pass
