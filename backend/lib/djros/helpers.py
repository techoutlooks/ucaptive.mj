# -*- coding: utf-8 -*-
__author__ = 'ceduth'


import re
import routeros_api
from .settings import get_setting
from .constants import *


def hyphen_to_underscore(name):
    return regexp.sub(r'_', name).lower()


def normalize_keys(fn, data):
    """ Normalize data (dict keys or list elts) to comply with python variables naming """

    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = fn(key)
            new_dict[new_key] = normalize_keys(fn, value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = normalize_keys(fn, data[i])
        return data
    return data

regexp = re.compile(r'[^a-zA-Z0-9]')


# Make RouterOS attrs names python compliant
hyphenate = lambda data: normalize_keys(hyphen_to_underscore, data)     # replace '-' in dict keys by underscore
booleanify = lambda s: s if isinstance(s, bool) else ROUTEROS_BOOL[s]   # replace 'true','false' by pythonic bool


class RouterOSConnector(object):
    """ 
    Controlled connection to RouterOS router. 
    Usage: 
        with RouterOSConnector() as ros_conn:
            ros_conn.some_method()
    """
    conn = None

    def __init__(self, ip_addr=None, username=None, password=None):
        self.ip_addr = ip_addr or get_setting('ROUTEROS_DEFAULT_IP')
        self.username = username or get_setting('ROUTEROS_DEFAULT_LOGIN')
        self.password = password or get_setting('ROUTEROS_DEFAULT_PASSWORD')

    def __enter__(self):
        self.conn = self.create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.disconnect()

    def create_connection(self):
        try:
            conn = routeros_api.RouterOsApiPool(host=self.ip_addr, username=self.username, password=self.password)
        except routeros_api.exceptions.RouterOsApiError, exc:
            # FIXME: do logging
            conn = None
        return conn


class RouterOSConnection(object):
    """
    Driver for managing Singleton IP connections to RouterOS.
    
    """
    # TODO: better exception handing, logging, caching connection
    # TODO: odbc connection to RouterOS

    params = None                   # ip_addr, username, password as dict
    connection = None               # RouterOS-API connection object
    api = None                      # RouterOS-API API object

    @classmethod
    def get_connection(cls, new=False):
        """Creates return new Singleton connection."""

        if new or not cls.connection:
            # TODO: validate connection params
            params = cls.params
            with RouterOSConnector(**params) as conn:
                cls.connection = conn
        return cls.connection

    @classmethod
    def execute_query(cls, command):
        """ Execute query on singleton connection """

        connection = cls.get_connection()
        try:
            api = connection.get_api()
        except Exception:
            connection = cls.get_connection(new=True)  # Create new connection
            api = connection.get_api()

        cursor = api.get_resource(command)
        return cursor