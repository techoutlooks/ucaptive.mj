# -*- coding: utf-8 -*-
"""
Django settings for Redis.

"""


class AbstractRedisCacheMixin(object):

    # we use a redis db of 10 for testing so that we maintain caches for dev
    # todo: REDIS_DB = 10 #if TESTING else 15
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 10

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "%s:%s:%s" % (REDIS_HOST, REDIS_PORT, REDIS_DB),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

    class Meta:
        abstract = True