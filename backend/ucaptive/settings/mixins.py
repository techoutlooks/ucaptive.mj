
from os.path import join, abspath
from configurations import values
from lib.settings.mixins import AbstractCeleryMixin


class CeleryMixin(AbstractCeleryMixin):
    """
    Django settings for django-cities-light

    """
    CELERY_ACCEPT_CONTENT = ['application/json', 'pickle']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    # CELERY_TIMEZONE = 'Africa/Nairobi'


class CitiesMixin(object):
    """
    Django settings for django-cities-light

    """

    ############################################
    # django-cities-light specifics

    # Behold our custom models
    CITIES_LIGHT_APP_NAME = 'cities'

    @property
    def CITIES_LIGHT_TRANSLATION_LANGUAGES(self):
        """ Same as settings.LANGUAGES """
        return list(map(lambda x: x[0], self.LANGUAGES))

    # Download geo data (countries, regions, cities) from below countries only
    CITIES_LIGHT_INCLUDE_COUNTRIES = values.Value(['GN'])

    @property
    def CITIES_LIGHT_CITY_SOURCES(self):
        return ['file://%s/%s/%s.zip' %(self.DATA_DIR, self.CITIES_LIGHT_APP_NAME, tld)
                for tld in self.CITIES_LIGHT_INCLUDE_COUNTRIES]

    @property
    def CITIES_LIGHT_DATA_DIR(self):
        return abspath(join(self.DATA_DIR, 'cities'))

    ############################################
    # Django specifics

    @property
    def LOGGING(self):
        logging = super(CitiesMixin,self).LOGGING
        logging['loggers'].update({
            'cities_light': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
            },
        })
        return logging

    @property
    def INSTALLED_APPS(self):
        return list(super(CitiesMixin, self).INSTALLED_APPS) + ['cities_light']


class DataImporterMixin(object):
    """ Basic Django configuration for our file-to-model mapper (data-importer)."""

    @property
    def IMPORTER_TEMPLATE_FILE(self):
        return join(self.MEDIA_ROOT, 'samples', 'ureporters.xls')
