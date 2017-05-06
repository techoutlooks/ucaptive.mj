# -*- coding: utf-8 -*-
__author__ = 'ceduth'


import json

from django.conf import settings
from rest_framework.parsers import JSONParser, ParseError, six

from ..helpers import hyphenate


class HyphenJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return hyphenate(json.loads(data))
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))