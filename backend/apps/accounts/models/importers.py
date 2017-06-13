# -*- coding: utf-8 -*-

from collections import OrderedDict
from lib.mixins.logging import WrapLoggerMixin

from data_importer.importers.generic import GenericImporter
from apps.accounts.models import Reporter, Profile
from apps.cities.models import Country, Region, City
from djra.freeradius.models import RadUser
from djra.freeradius.settings import get_setting


class UReportDataImporter(WrapLoggerMixin, GenericImporter):
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

    def import_user(self, **row):
        """         
        Update or create User from xls row.
        """
        row = Reporter.parse_model_data(**row)
        user_lookup = {'mobile_number': str(row.pop('mobile_number'))}
        user = None
        existed = False

        # Ignore lines missing lookup fields
        for key in user_lookup.iterkeys():
            if not user_lookup.get(key, ''):
                return existed, user

        # Update or create user instance
        try:
            user = Reporter.objects.get(**user_lookup)
            existed = True
            if row:
                for k, v in row.items():
                    setattr(user, k, v)
                user.save()

        except Reporter.DoesNotExist:
            user_lookup.update(row)
            try:
                user = Reporter(**user_lookup)
                user.save()
            except Exception as e:
                self.log_error("Failed ... saving reporter {user} !", user=user, exc_info=True)
                print "Failed ... saving user {user} {msg} !".format(user=user, msg=e.message)

            else:
                self.log_debug("Success ... saving user {user} !", user=user)
                print "Success ... saving user {user}!".format(user=user)

        return existed, user

    def import_user_profile(self, user=None, **row):
        """ 
        Update or create User profile from xls row 
        """
        profile = None
        if user:
            user_lookup = {'reporter': user}
            try:
                # fk_fields lookup from raw data
                row = Profile.parse_model_data(**row)
                location = dict(country='', region='', city='')

                location['country'] = Country.objects.filter(name__icontains='Guinea').first()
                location['region'] = Region.objects.filter(name__icontains=row.get('region')).first()
                location['city'] = City.objects.filter(name__icontains=row.get('city')).first()
                self.log_warning("Failed ... parsing location for user {user}", user=user, exc_info=True)

                # fk_fields update
                row.update(user_lookup)
                row.update(location)

                # TODO: implement signal instead (empty profile created by signal gets updated here)
                profile = Profile.update_or_create(defaults=row, **user_lookup)
            except Exception as e:
                self.log_error("Failed ... creating profile for user {user} !", user=user, exc_info=True)
                print "Failed ... creating profile for user {user} {msg} !".format(user=user, msg=e.message)

        return profile

    # def is_valid(self):
    #     return all((
    #         self.importer.is_valid(),
    #     ))

    def save(self, instance=None):
        total_counts = dict(users=0, wifi_users=0, profiles=0, existed=0)
        msg = "Done ... importing/updating {users} users, {profiles} profiles ({existed} existed) " \
              " and {wifi_users} WiFi accounts from xls file {file}."

        for row_num, data in self.cleaned_data:
            self.log_debug("Processing ... importing xls line #{num} !", num=row_num)
            existed, user = self.import_user(**data)
            if existed:
                total_counts['existed'] += 1

            if user:

                # create linked user profile
                total_counts['users'] += 1
                profile = self.import_user_profile(user=user, **data)
                if profile:
                    total_counts['profiles'] += 1

                # also, create RadUser from user in default group with default password
                # if not defined in settings, then default password is same as username
                raduser_data = {}
                user_data = Reporter.parse_model_data(**data)
                raduser_data['username'] = user_data.get('mobile_number')
                raduser_data['password'] = user_data.get('password', get_setting('DEFAULT_PASSWORD')
                                                         or raduser_data['username'])
                groups = get_setting('DEFAULT_GROUPS')
                raduser_data.update({'groups': groups})
                try:
                    RadUser.objects.create(**raduser_data)
                except Exception as e:
                    self.log_error("Failed ... creating/updating xls radius user account !")
                    print "Failed ... creating/updating xls radius user account: {msg}".format(msg=e.message)
                else:
                    total_counts['wifi_users'] += 1

        self.log_info(msg, users=total_counts['users'], wifi_users=total_counts['wifi_users'],
                      profiles=total_counts['profiles'], existed=total_counts['existed'], file=self.source)

        print msg.format(users=total_counts['users'], wifi_users=total_counts['wifi_users'],
                         profiles=total_counts['profiles'], existed=total_counts['existed'], file=self.source)

            # try:
            #     user = self.update_or_create_reporter(**data)
            #     if user:
            #         self.update_or_create_profile(user=user, **data)
            #
            # except Exception as e:
            #     self.log_error("Failed ... importing xls line #{num} !", num=row_num)
            #     print "Failed ... importing xls line #{num}: {err}".format(num=row_num, err=e.message)
            # else:
            #     self.log_info("Success ... importing xls line #{num} !", num=row_num)
            #     print "Success ... importing xls line #{num} !".format(num=row_num)
            #
