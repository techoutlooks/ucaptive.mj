# -*- coding: utf-8 -*-
"""
Strings and formatting utilities.

"""
import datetime
import pytz
import six
import random, string


ISO8601_DATE_FORMAT = '%Y-%m-%d'
ISO8601_DATETIME_FORMAT = ISO8601_DATE_FORMAT + 'T' + '%H:%M:%S'

# Lambdas

srandom = lambda length: ''.join(random.sample(string.lowercase+string.digits, length))


# Functions

def parse_iso8601(value):
    """
    Parses a datetime as a UTC ISO8601 date
    """
    if not value:
        return None

    if 'T' in value:  # has time
        _format = ISO8601_DATETIME_FORMAT

        if '.' in value:  # has microseconds. Some values from RapidPro don't include this.
            _format += '.%f'
        if 'Z' in value:  # has zero offset marker
            _format += 'Z'
    else:
        _format = ISO8601_DATE_FORMAT

    return datetime.datetime.strptime(value, _format).replace(tzinfo=pytz.utc)


def format_iso8601(value):
    """
    Formats a datetime as a UTC ISO8601 date
    """
    _format = ISO8601_DATETIME_FORMAT + '.%f'

    return six.text_type(value.astimezone(pytz.UTC).strftime(_format))




