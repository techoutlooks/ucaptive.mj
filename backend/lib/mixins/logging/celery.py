from __future__ import absolute_import

import logging
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


class WrapTaskLoggerMixin(object):
    """ Mixin that wraps a logger for Celery Task subclasses """

    def log_debug(self, *args, **kwargs):
        return self.wrap_logger(logging.DEBUG, *args, **kwargs)

    def log_error(self, *args, **kwargs):
        return self.wrap_logger(logging.ERROR, *args, **kwargs)

    def log_info(self, *args, **kwargs):
        return self.wrap_logger(logging.INFO, *args, **kwargs)

    def log_warning(self, *args, **kwargs):
        return self.wrap_logger(logging.WARNING, *args, **kwargs)

    def wrap_logger(self, level, msg, exc_info=False, *args, **kwargs):
        kwargs.setdefault('task', self.__name__)
        full_msg = msg.format(*args, **kwargs)
        logger.log(level, full_msg, exc_info=exc_info)
        return full_msg




