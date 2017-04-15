# -*- coding: utf-8 -*-
"""
Celery settings.

"""

from .caching import AbstractRedisCacheMixin


class AbstractCeleryMixin(AbstractRedisCacheMixin):
    """
    Basic Django settings for Celery as an abstract configuration class.
    Do not import AbstractRedisCacheMixin if importing me.

    """
    # todo: make broker (redis, rabbitmq, etc.) configurable

    # -----------------------------------------------------------------------------------
    # Celery configuration for initializing by setup()
    # -----------------------------------------------------------------------------------
    # BROKER_URL
    # CELERY_RESULT_BACKEND
    # OUTGOING_PROXIES :The URL and port of the proxy server to use when needed (if any, in requests format)

    BROKER_URL = None
    CELERY_RESULT_BACKEND = None
    HOSTNAME = None
    OUTGOING_PROXIES = {}

    class Meta:
        abstract = True

    @classmethod
    def get_redis_opts(cls, args):
        """
        Fetch values for given args from redis configuration.

        """
        get_redis_arg = lambda arg: getattr(super(AbstractCeleryMixin, cls), 'REDIS_%s' % arg)
        return dict(zip(args, map(lambda arg: get_redis_arg(arg), args)))

    @classmethod
    def setup_redis_cache(cls):
        """
        Initialize

        """
        args = ['HOST', 'PORT', 'DB']
        redis_opts = cls.get_redis_opts(args)
        cls.BROKER_URL = 'redis://%s:%d/%d' % (redis_opts['HOST'],
                                               redis_opts['PORT'],
                                               redis_opts['DB'])
        cls.CELERY_RESULT_BACKEND = cls.BROKER_URL
        cls.HOSTNAME = "localhost"

    def __init__(self, *args, **kwargs):
        self.setup_redis_cache()