from dal import autocomplete

from .models import Country, Region, City


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class RegionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Region.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = 100

    def get_queryset(self):
        qs = City.objects.all()
        region = self.forwarded.get('region', None)
        if region:
            qs = qs.filter(region=region)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs