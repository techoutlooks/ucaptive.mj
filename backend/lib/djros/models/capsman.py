# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from django.db import models
from django.apps import apps
from django.forms.models import model_to_dict
from lib.mixins.models import ModelFactoryMixin
from lib.mixins.logging import WrapLoggerMixin
from ..helpers import hyphenate, booleanify, RouterOSConnection
from .. import settings as djros_settings

from apps.orgs.models import Org


class CapsManConnectionMgr(WrapLoggerMixin, ModelFactoryMixin):
    """ 
    CAPsMAN Primitives & IP network connectivity manager.
    Expects valid ip_addr,logi,password in 'params' or 'connection_string'.
         
    """
    # TODO: logging wrapper

    def __init__(self, capsman, *args, **kwargs):

        # per CAPsMAN singleton connection
        # returns or create (if necessary) the same and unique RouterOSConnection obj per CAPsMAN
        params = dict(ip_addr=capsman.ip_addr, username=capsman.username, password=capsman.password)
        connection_class_name = "%sROSConn" % str(capsman.name)
        connection_class = type(connection_class_name, (RouterOSConnection,), {'params': params})
        self.connection = connection_class()
        self.capsman = capsman

    # ORM-agnostic CAPsMAN primitives (queries).
    # Primitives rely on RouterOSConnection.execute_query() to perform API calls based on singleton connection.
    # Don't call RouterOSConnection.get_connection() directly unless for override.

    def fetch_caps(self, type, active_only=False):
        """ Retrieve CAPs of type from CAPsMAN as Cap objects list. """
        # TODO: by status, etc.

        caps = []
        cmd = djros_settings.get_setting('CAPSMAN_CAP_TYPES')[type]['cmd']
        caps_model = djros_settings.get_setting('CAPSMAN_CAP_TYPES')[type]['model']
        caps_data = self.connection.execute_query(cmd).get()
        for cap_data in caps_data:
            try:
                caps_data = hyphenate(caps_data)
                cap_validated_data = self.parse_model_data(model=caps_model, exclude=('id',), **cap_data)
                cap = Cap(**cap_validated_data)
                cap.capsman = self.capsman
            except Exception:
                self.log_error("Fetching CAP {cap_data} ... Failed !", cap_data=cap_data)
            else:
                caps.append(cap)
                self.log_debug("Done ..... Fetching CAP {cap_name}.", cap_name=cap.name)

        return caps

    def fetch_radios(self, for_cap=None):
        """ Retrieve radios (all, for_cap) in CAPsMAN """

        radios = []

        # this fetches all radios, regardless of cap, as python dict
        radios_model = apps.get_model('djros.Radio')
        cmd = djros_settings.CAPSMAN_GET_RADIOS_CMD
        radios_data = self.connection.execute_query(cmd).get()

        # now, clean data, convert to Cap obj,
        # and attach serving cap
        for radio_data in radios_data:
            try:
                radio_data = hyphenate(radio_data)
                radio_validated_data = self.parse_model_data(model=radios_model, exclude=('id',), **radio_data)
                radio = radios_model(**radio_validated_data)
                if for_cap:
                    radio.cap = for_cap

            except Exception:
                self.log_error("Failed ... Fetching Radio {radio}. !", radio=radio_data)
            else:
                radios.append(radio)
                self.log_debug("Done ..... Fetching CAP {radio}.", radio=radio.interface)

        return radios


class CapsManQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class CapsManManager(ModelFactoryMixin, models.Manager):
    def get_queryset(self):
        return CapsManQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def by_org(self, org):
        return self.filter(org=org) if org.is_active else None


class CapsMan(WrapLoggerMixin, ModelFactoryMixin, models.Model):
    """
    A CAPsMAN instance at an organization.

    """
    org = models.ForeignKey(Org, related_name='capsmans')
    name = models.CharField(max_length=100, help_text="The backend's name")

    # TODO: Password model field: http://stackoverflow.com/questions/9324432/how-to-create-password-input-field-in-django
    # TODO: Validation: http://stackoverflow.com/questions/30295246/django-genericipaddress-field-is-not-validating-input
    ip_addr = models.GenericIPAddressField(protocol='IPv4', help_text="FQDN of the billing host at the orgs's.")
    username = models.CharField(max_length=100, help_text="Valid username to authenticate with CAPsMAN.")
    password = models.CharField(max_length=100, help_text="Valid password to authenticate with CAPsMAN.")
    is_active = models.BooleanField(default=True)

    # non field
    connection_mgr_class = CapsManConnectionMgr

    objects = CapsManManager()

    def __unicode__(self):
        return '{name} ({ip_addr}) @{org}'.format(name=self.name, ip_addr=self.ip_addr, org=self.org)

    def get_org(self, id):
        """ Get Org obj from pk"""
        return self.org

    def get_connection(self, *args, **kwargs):
        """
        Return the connection manager instance that should be used for connecting to this CAPsMAN,
        and for carrying on generic operations.
        """
        return self.get_connection_mgr().connection

    def get_connection_mgr(self, *args, **kwargs):
        """
        Return the connection manager instance that should be used for connecting to this CAPsMAN,
        and for carrying on generic operations.
        """
        connection_mgr_class = self.get_connection_mgr_class()
        return connection_mgr_class(self, *args, **kwargs)

    def get_connection_mgr_class(self):
        """
        Return the class that knows how to connect to CAPsMAN over IP network.
        Defaults to using `self.connection_class`.
        """
        assert self.connection_mgr_class is not None, (
            "'%s' should either include a `connection_mgr_class` attribute, "
            "or override the `get_connection_mgr_class()` method."
            % self.__class__.__name__
        )
        return self.connection_mgr_class

    def sync_remote_caps(self):
        """ Sync remote caps """
        return self.sync_caps(type=djros_settings.CAPSMAN_CAP_TYPE_REMOTE)

    def sync_interface_caps(self):
        """ Sync caps interfaces """
        return self.sync_caps(type=djros_settings.CAPSMAN_CAP_TYPE_INTERFACE)

    def sync_caps(self, type):
        """ Retrieve caps from CAPsMAN at RouterOS and save them to db, deleting stale caps. """

        model_lookup_field = djros_settings.get_setting('CAPSMAN_CAP_TYPES')[type]['model_lookup_field']
        cap_model = djros_settings.get_setting('CAPSMAN_CAP_TYPES')[type]['model']
        related_manager = filter(lambda mgr: mgr.model == cap_model, self.get_related_managers())[0]

        current_caps = self.get_connection_mgr().fetch_caps(type=type)
        old_caps = related_manager.all()

        # id(s) = value(s) from model_lookup_field
        old_caps_ids = [getattr(c, model_lookup_field) for c in old_caps]
        current_caps_ids = [getattr(c, model_lookup_field) for c in current_caps]

        # delete stale caps
        if set(old_caps_ids) != set(current_caps_ids):
            to_delete_ids = set(old_caps_ids) - set(current_caps_ids)
            to_delete_query = {"{}__in".format(model_lookup_field): list(to_delete_ids)}
            old_caps.filter(**to_delete_query).delete()

        # update current caps
        ignore_fields_on_update = ['id', 'capsman']
        for p, cap in enumerate(current_caps):
            cap_kwargs = {"{}".format(model_lookup_field): getattr(cap, model_lookup_field),
                          'capsman': self, # has to be obj, not id
                          }
            rup,created = self.caps.update_or_create(defaults=model_to_dict(cap, exclude=ignore_fields_on_update),
                                                     **cap_kwargs)
            rup.save()

        return len(current_caps)

    def get_cap_for_radio(self, radio):
        """ Find cap serving given radio. """

        model_lookup_field = djros_settings.get_setting('CAPSMAN_RADIOS_LOOKUP_FIELD')
        cap_ptr_field = djros_settings.get_setting('CAPSMAN_RADIOS_CAP_PTR_FIELD')
        cap_lookup_kwargs = {"{}".format(cap_ptr_field): getattr(radio, model_lookup_field)}
        return self.caps.filter(**cap_lookup_kwargs).first()

    def sync_radios(self):
        """ Retrieve all radios in CAPsMAN at RouterOS (respective of CAP), and save them to db deleting old ones. """

        radios = []
        radios_model = apps.get_model('djros.Radio')

        # this fetches all radios, regardless of cap, as python dict
        # and attach serving cap before saving to db

        for radio in self.get_connection_mgr().fetch_radios():
            radio.cap = self.get_cap_for_radio(radio)
            radios.append(radio)

        # delete stale radios,
        # and bulk create new ones
        try:
            radios_model.objects.all().delete()
            radios_model.objects.bulk_create(radios)
        except Exception:
            self.log_error("Failed ... saving {count} radios.", count=len(radios))

        self.log_debug("Done ..... Fetching {count}.", count=len(radios))
        return len(radios)


class CapQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(disabled=False)


class Cap(ModelFactoryMixin, models.Model):
    """ 
    Static AP controlled by CAPsMAN.
    CMD = /capsman/interface

    """

    # interface config
    name = models.CharField(max_length=64)                      # ties cap to radio (actually radio lookup field)
    radio_mac = models.CharField(max_length=64, unique=True)    # CAPsMAN distinguishes between actual wireless interfaces
    mac_address = models.CharField(max_length=64)               # (radios) based on their builtin MAC address (radio-mac)
    master_interface = models.CharField(max_length=64)
    bound = models.BooleanField(default=False)                  # provisioned ?

    # status related,
    # either boolean, or not present
    running = models.BooleanField(default=False)
    inactive = models.BooleanField(default=True)
    disabled = models.BooleanField(default=True)
    current_channel = models.CharField(max_length=64)

    # related resources
    capsman = models.ForeignKey(CapsMan, related_name='caps')

    objects = CapQuerySet.as_manager()

    def clean(self):
        """ Model validation fired by presave signal @signals.run_clean() """

        # convert Mikrotik bool to Python bool
        status_field_names = ('bound', 'running', 'inactive', 'disabled')
        map(lambda x: setattr(self, x, booleanify(getattr(self, x))), status_field_names)

    def __unicode__(self):
        return '{name} ({mac})'.format(name=self.name, mac=self.radio_mac)


class RemoteCap(models.Model):
    """ 
    An AP dynamically controlled by CAPsMAN.
    CMD = /capsman/remote-cap
    
    """
    # config attrs
    name = models.CharField(max_length=64)
    identity = models.CharField(max_length=64)
    radios = models.IntegerField()
    base_mac = models.CharField(max_length=64, unique=True)
    state = models.CharField(max_length=64)
    # id = models.CharField(max_length=64)

    # hardware info attrs
    version = models.CharField(max_length=64)
    board = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    # related resources, not CAPsMAN attrs
    capsman = models.ForeignKey(CapsMan, related_name='remote_caps')
    disabled = models.BooleanField(default=True)

    objects = CapQuerySet.as_manager()


class Radio(models.Model):
    """
    Client connected to Cap. Read-only & active status.
    CMD = /capsman/registration-table

    """

    # own attrs
    uptime = models.CharField(max_length=64)
    rx_signal = models.CharField(max_length=64)
    tx_rate = models.CharField(max_length=64)
    rx_rate = models.CharField(max_length=64)
    tx_rate_set = models.CharField(max_length=64)
    ssid = models.CharField(max_length=64)
    packets = models.CharField(max_length=64)
    bytes = models.CharField(max_length=64)

    # radio attrs linking to other models
    interface = models.CharField(max_length=64)                 # lookup field for parent cap
    mac_address = models.CharField(max_length=64)               # uniquely identifies radios
    cap = models.ForeignKey(Cap, related_name='radios')         # base station (cap)


