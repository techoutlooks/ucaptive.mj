
from django.db import models
from django.core.urlresolvers import reverse

from cities_light.settings import ICountry
from cities_light.receivers import connect_default_signals
from cities_light.signals import country_items_post_import
from cities_light.abstract_models import (AbstractCountry, AbstractRegion, AbstractCity)


class Country(AbstractCountry):

    def get_absolute_url(self):
        return reverse('by_country', kwargs={'country_slug': self.slug})
connect_default_signals(Country)


class Region(AbstractRegion):
    """ eg. Guinea has 8 natural regions. """

    def get_absolute_url(self):
        return reverse('by_region', kwargs={'country_slug': self.country.slug,
                                            'region_slug': self.slug})
connect_default_signals(Region)


class City(AbstractCity):

    def get_absolute_url(self):
        return reverse('by_region', kwargs={'country_slug': self.country.slug,
                                            'region_slug': self.region.slug,
                                            'place_slug': self.slug})
connect_default_signals(City)

#
# def process_country_import(sender, instance, items, **kwargs):
#     instance.capital = items[ICountry.capital]
#
# country_items_post_import.connect(process_country_import)