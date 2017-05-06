from django.conf.urls import patterns, include, url
from .views import CountryAutocomplete, RegionAutocomplete, CityAutocomplete


urlpatterns = [
    url(r'^country-autocomplete/$', CountryAutocomplete.as_view(), name='country-autocomplete'),
    url(r'^region-autocomplete/$', RegionAutocomplete.as_view(), name='region-autocomplete'),
    url(r'^city-autocomplete/$', CityAutocomplete.as_view(), name='city-autocomplete'),
]