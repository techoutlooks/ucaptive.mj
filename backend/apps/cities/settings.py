from os.path import abspath, join, dirname
from configurations import values


class CitiesSettingsMixin(object):
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
        logging = super(CitiesSettingsMixin, self).LOGGING
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
        """ Add django-cities-light app and django-autocomplete-light aka dal. """
        existing_apps = super(CitiesSettingsMixin, self).INSTALLED_APPS
        cities_apps = ('dal', 'dal_select2', 'cities_light')
        return self.add_apps(cities_apps, existing_apps)
