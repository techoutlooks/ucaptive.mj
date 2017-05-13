# -*- coding: utf-8 -*-

from collections import OrderedDict

from data_importer.importers.generic import GenericImporter

from apps.accounts.models import Reporter, Profile
from apps.cities.models import Country, Region, City


class UReportDataImporter(GenericImporter):
    """
    Import csv, xls, xlsx data into the Reporter and related models.

    """
    fields = OrderedDict((
        ('age', 'E'),
        ('gender', 'F'),

        # fk_fields, need related model lookup
        ('city', 'G'),
        ('region', 'H'),
        ('country', 'I'),
        ('mobile_number', 'A'),
        ('first_name', 'B'),
        ('last_name', 'C'),
        ('email', 'D'),


    ))

    class Meta:
        ignore_first_line = True
        model = None

    def update_or_create_reporter(self, **row):
        row = Reporter.parse_model_data(**row)
        user = None
        try:
            user_lookup = {'mobile_number': row.get('mobile_number')}
            user = Reporter.update_or_create(defaults=row, **user_lookup)
        except:
            print "unknown error importing reporter !"
        return user

    def update_or_create_profile(self, **row):
        print " *** row=%s *** " % row

        user_lookup = {'reporter': self.update_or_create_reporter(**row)}
        profile = None
        try:
            # fk_fields lookup from raw data
            row = Profile.parse_model_data(**row)
            country = Country.objects.get(name='Guinea')
            region = Region.objects.get(name=row.get('region'))
            city = City.objects.get(name=row.get('city'))
            place = {
                'country': country,
                'region': region,
                'city': city
            }
            # fk_fields update
            row.update(user_lookup)
            row.update(place)

            profile = Profile.update_or_create(defaults=row, **user_lookup)
        except:
            print "unknown error importing a reporter profile !"

        return profile

    # def is_valid(self):
    #     return all((
    #         self.importer.is_valid(),
    #     ))

    def save(self):
        for row_num, data in self.cleaned_data:
            try:
                print "data={}".format(data)
                self.update_or_create_profile(**data)
            except Exception as e:
                print "Unknown error %s importing xls line {} !".format(row_num) %e
            else:
                print "Success importing xls line {}".format(row_num)
