# -*- coding: utf-8 -*-
"""
User

"""
from __future__ import unicode_literals

import json
from django_redis import get_redis_connection


def get_cacheable(cache_key, cache_ttl, callable, r=None, force_dirty=False):
    """
    Gets the result of a method call, using the given key and TTL as a cache
    """
    if not r:
        r = get_redis_connection()

    if not force_dirty:
        cached = r.get(cache_key)
        if cached is not None:
            return json.loads(cached)

    calculated = callable()
    r.set(cache_key, json.dumps(calculated), cache_ttl)

    return calculated


def get_cacheable_result(cache_key, cache_ttl, callable, r=None, force_dirty=False):
    """
    Gets a cache-able integer calculation result
    """
    return int(get_cacheable(cache_key, cache_ttl, callable, r=r, force_dirty=force_dirty))


def incrby_existing(key, delta, r=None):
    """
    Update a existing integer value in the cache. If value doesn't exist, nothing happens. If value has a TTL, then that
    is preserved.
    """
    if not r:
        r = get_redis_connection()

    lua = "local ttl = redis.call('pttl', KEYS[1])\n" \
          "local val = redis.call('get', KEYS[1])\n" \
          "if val ~= false then\n" \
          "  val = tonumber(val) + ARGV[1]\n" \
          "  redis.call('set', KEYS[1], val)\n" \
          "  if ttl > 0 then\n" \
          "    redis.call('pexpire', KEYS[1], ttl)\n" \
          "  end\n" \
          "end"
    r.eval(lua, 1, key, delta)
    

# integrate below

from django.core.cache import cache


class WrapCacheMixin(object):

    def cache_add(self, *args, **kwargs):
        return self.wrap_cache("add", *args, **kwargs)

    def cache_delete(self, *args, **kwargs):
        return self.wrap_cache("delete", *args, **kwargs)

    def cache_get(self, *args, **kwargs):
        return self.wrap_cache("get", *args, **kwargs)

    def cache_incr(self, *args, **kwargs):
        return self.wrap_cache("incr", *args, **kwargs)

    def cache_set(self, *args, **kwargs):
        return self.wrap_cache("set", *args, **kwargs)

    def wrap_cache(self, method, org, key, *args, **kwargs):
        cache_key = key.format(task=self.__name__, org=org.pk)
        return getattr(cache, method)(cache_key, *args, **kwargs)

