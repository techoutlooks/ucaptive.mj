# -*- coding: utf-8 -*-
__author__ = 'ceduth'


import datetime
from lib.settings.mixins import AbstractCeleryMixin


class OrgTaskSettingsMixin(AbstractCeleryMixin):
    """
    Django settings for Org Tasks

    """

    ############################################
    # Celery settings
    # FIXME: CELERY_ALWAYS_EAGER not suitable for production

    CELERY_ACCEPT_CONTENT = ['application/json', 'pickle']
    CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_TIMEZONE = 'Africa/Conakry'
    BROKER_URL = CELERY_RESULT_BACKEND = 'redis://localhost:6379/4'
    CELERYD_HIJACK_ROOT_LOGGER = False
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_SEND_TASK_ERROR_EMAILS = True
    CELERY_ALWAYS_EAGER = True                                      # task not queued, but blocking until it returns.

    ############################################
    # Settings and scheduler for all tasks in this project.

    ORG_TASK_TIMEOUT = datetime.timedelta(seconds=10)

    @classmethod
    def _backend_scheduler_task(cls, task_name):
        return {
            'task': 'apps.orgs.tasks.ScheduleTaskForActiveOrgs',
            'schedule': cls.ORG_TASK_TIMEOUT,
            'kwargs': {
                'task_name': task_name,
            },
        }

    @classmethod
    def CELERYBEAT_SCHEDULE(cls):
        return {
            # Per each orgs, do below syncs
            'sync-models': cls._backend_scheduler_task('djros.tasks.SyncCapsMan'),
        }
