# -*- coding: utf-8 -*-
"""
U-Reporter user model.

U-Reporters log in with their mobile phone numbers (USERNAME_FIELD).
Their mobile phone number is also used to register a radius (Freeradius v3) user account.
U-Reporters have a profile (Profile) storing additional user information and preferences.
Radius (raduser table) and Profile are filled using signals.

"""
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_redis import get_redis_connection
from filer.fields.image import FilerImageField
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey

from one_accounts.models import OneUserManager, AbstractOneUser
from lib.mixins.models import ModelFactoryMixin

from apps.cities.models import Country, Region, City
from .user_constants import *
from .users_limits import Plan
from ..constants import GENDER_CHOICES


class UserManager(OneUserManager):
    use_in_migrations = True

    def _create_user(self, mobile_number, password, **extra_fields):
        """
        Creates and saves a User given his phone number and password.

        """
        if not mobile_number:
            raise ValueError(_('You must provide your U-Reporter\'s mobile phone number'))

        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('date_joined', datetime.now())
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


@python_2_unicode_compatible
class Reporter(ModelFactoryMixin, AbstractOneUser):
    """
    A U-Reporter's system account.

    login = E.164 phone format, password =

    """

    # Whether this user can access the admin site.
    @property
    def is_staff(self):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, bool):
        self.is_admin = bool

    # org = models.ForeignKey('orgs.Org')
    mobile_number = PhoneNumberField(unique=True)
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('u-reporter')
        verbose_name_plural = _('u-reporters')

    def __str__(self):
        return str(self.mobile_number)

    def clean(self):
        """ 
        Some cleaning for Reporter instance prior saving:
        - Make Reporter field not mandatory (to None if exists)
        
        Fired by presave signal @signals.run_clean() 
        """
        if self.email and Reporter.objects.filter(email=self.email).exists():
            self.email = None

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        pass

    def update_caches(self, event, entity):
        """
        Update user-level caches in response to an event
        """
        r = get_redis_connection()

        if event in [UserEvent.topup_new, UserEvent.topup_updated]:
            r.delete(USER_CREDITS_TOTAL_CACHE_KEY % self.pk)
            r.delete(USER_CREDITS_PURCHASED_CACHE_KEY % self.pk)
            r.delete(USER_ACTIVE_TOPUP_KEY % self.pk)
            r.delete(USER_CREDIT_EXPIRING_CACHE_KEY % self.pk)
            r.delete(USER_LOW_CREDIT_THRESHOLD_CACHE_KEY % self.pk)

            for topup in self.topups.all():
                r.delete(USER_ACTIVE_TOPUP_REMAINING % (self.pk, topup.pk))

    def clear_caches(self, caches):
        """
        Clears the given cache types (currently just credits) for this user. Returns number of keys actually deleted
        """
        if UserCache.credits in caches:
            r = get_redis_connection()

            active_topup_keys = [USER_ACTIVE_TOPUP_REMAINING % (self.pk, topup.pk) for topup in self.topups.all()]
            return r.delete(USER_CREDITS_TOTAL_CACHE_KEY % self.pk,
                            USER_CREDITS_USED_CACHE_KEY % self.pk,
                            USER_CREDITS_PURCHASED_CACHE_KEY % self.pk,
                            USER_ACTIVE_TOPUP_KEY % self.pk,
                            **active_topup_keys)
        else:
            return 0


@python_2_unicode_compatible
class Profile(ModelFactoryMixin, models.Model):
    """
    User profile of a U-Reporter

    """
    # tod: fix filer migration issue with photo field

    # personal info.
    reporter = models.OneToOneField(Reporter, on_delete=models.CASCADE, related_name='profile')
    # photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True, related_name='+')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text=_("Sex"))
    time_spend = models.DurationField(default=timedelta(), null=True, blank=True,
                                      help_text=_('Total connection time.'))
    # geo properties from the 'cities' app.
    # already exist in related models, don't create new.
    country = models.ForeignKey(Country, null=True, default=1, help_text=_("What country are you from?"))
    region = models.ForeignKey(Region, null=True, help_text=_("What region are you from?"))
    city = models.ForeignKey(City, null=True, help_text=_("Your birth place."))
    # accounting fields
    plan = models.ForeignKey(Plan, null=True, blank=True)

    def __str__(self):
        # todo: ugettext_lazy support with "".format.
        return "{age} years old {gender} from {city}, {region}. Spent {time} online".\
            format(age=self.age, gender=self.gender, region=self.region, city=self.city, time=self.time_spend)

    # @classmethod
    # def create_by_import(cls, **kwargs):
    #     """
    #
    #     eg. when creating Profile's from an csv/xls/xls file import.
    #     """
    #
    #     if kwargs:
    #         print "1. kwargs=%s" % kwargs
    #
    #         # build kwargs that create fk_models from strings
    #         # non fk fields already in kwargs, ready for saving
    #
    #         fk_models = cls.get_fk_models()
    #         ro_fields = ['country', 'region', 'city', 'plan']
    #         related_fields = ['mobile_number', 'first_name', 'last_name', 'email']
    #         for model in fk_models:
    #
    #             # scan every fk_field in fk_model
    #             model_kwargs = cls.get_related_fields_from_dict(model, **kwargs)
    #             print "model=%s. model_kwargs=%s" % (model, model_kwargs)
    #
    #             for prop in list(model_kwargs):
    #
    #                 # read only fk_fields don't need new instances to be created for them.
    #                 # instead, only affect the looked up instance to the fk_field
    #                 # hopefully, our ro_fields are all looked up by name attribute ...
    #                 if prop in ro_fields:
    #                     obj = cls.get_fk_instance(prop, {'name': model_kwargs.get(prop)})
    #
    #                 # some fk_fields in kwargs do not belong to this model,
    #                 # additionally they might be updated or created
    #                 # eg. 'mobile_number' belongs to one_accounts.Reporter
    #                 elif prop in related_fields:
    #                     obj = cls.update_or_create_related(prop, model, **model_kwargs)
    #
    #                 # updated fk_field
    #                 kwargs.update({prop: obj})
    #
    #     print "2. kwargs=%s" % kwargs
    #     return kwargs






