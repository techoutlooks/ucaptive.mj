from __future__ import unicode_literals

import datetime
# import logging

from celery import signature
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger

from django.apps import apps
from django.conf import settings
# from django.org.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from djcelery_transactions import PostTransactionTask
from celery import Task

# from ucaptive import celery_app
from ucaptive.celery import app as celery_app
from lib.utils.format import parse_iso8601, format_iso8601
from lib.mixins.logging import WrapTaskLoggerMixin
from lib.mixins.caching import WrapCacheMixin


FAILURE_COUNT = 'failure_count:{task}:{org}'
LAST_RUN_TIME = 'last_run_time:{task}:{org}'
ORG_TASK_LOCK = 'org_task:{task}:{org}'
LOCK_TIMEOUT = (settings.ORG_TASK_TIMEOUT * 12).seconds
RUNS_TIMEOUT = datetime.timedelta(days=7).seconds
MAX_TIME_BETWEEN_RUNS = datetime.timedelta(days=1)


class ScheduleTaskForActiveOrgs(WrapTaskLoggerMixin, PostTransactionTask):
    """ 
    Sync all active orgs, using the org's Backend. 
    
    """
    def apply_async(self, *args, **kwargs):
        kwargs.setdefault('queue', 'org_scheduler')
        kwargs.setdefault('expires', datetime.datetime.now() + settings.ORG_TASK_TIMEOUT)
        return super(ScheduleTaskForActiveOrgs, self).apply_async(*args, **kwargs)

    def run(self, task_name):
        """Schedule the OrgTask to be run for each active org."""

        if task_name not in celery_app.tasks:
            self.log_error(task_name, "No such task is registered.")
            return None

        self.log_info(task_name, "Scheduling task for each active org.")
        for org in apps.get_model('orgs', 'Org').objects.all():
            if not org.is_active:
                msg = "Skipping for org {org} because it is inactive."
                self.log_info(task_name, msg, org=org.name)
            else:
                signature(task_name, args=[org.pk]).delay()
                msg = "Scheduled for {org}."
                self.log_debug(task_name, msg, org=org.name)

        self.log_info(task_name, "Finished scheduling task for each active org.")

    def wrap_logger(self, level, org_task, msg, *args, **kwargs):
        kwargs.setdefault('org_task', org_task)
        msg = '{task} for {org_task}: ' + msg
        return super(ScheduleTaskForActiveOrgs, self).wrap_logger(level, msg, *args, **kwargs)


class OrgTask(WrapCacheMixin, WrapTaskLoggerMixin, PostTransactionTask):
    """
    Scaffolding to CREATE a task that operates on a single org.
    Runs OrgTask.org_task() every 'settings.BACKEND_TASK_TIMEOUT' minutes.

    """
    abstract = True

    def org_task(self, org):
        """ Celery Task scheduler callback. For Overriding. """
        raise NotImplementedError("Class must define the action to take on the org.")

    def apply_async(self, *args, **kwargs):
        kwargs.setdefault('expires', datetime.datetime.now() + settings.ORG_TASK_TIMEOUT)
        time_limit = settings.ORG_TASK_TIMEOUT.seconds
        kwargs.setdefault('time_limit', time_limit + 60)
        kwargs.setdefault('soft_time_limit', time_limit)
        kwargs.setdefault('max_retries', 0)
        return super(OrgTask, self).apply_async(*args, **kwargs)

    def check_rate_limit(self, org):
        """Return the next run time if this task has run too recently."""
        now = timezone.now()
        last_run_time = self.cache_get(org, LAST_RUN_TIME)
        if last_run_time is not None:
            # Calculate when the task will be eligible to run again.
            last_run_time = parse_iso8601(last_run_time) if last_run_time else None
            failure_count = self.cache_get(org, FAILURE_COUNT, default=0)
            delta = settings.ORG_TASK_TIMEOUT * 2 ** failure_count
            next_run_time = last_run_time + delta
            if now < next_run_time:
                # Task has been run too recently.
                raise ValueError(
                    "Skipping task because rate limit was exceeded. "
                    "Last run time was {}. "
                    "Task has failed {} times recently. "
                    "Task won't be run again before {}.".format(
                        last_run_time, failure_count, next_run_time))

        # Set the current time as the last run time.
        self.cache_set(org, LAST_RUN_TIME, value=format_iso8601(now), timeout=RUNS_TIMEOUT)

    def fail_count_incr(self, org):
        """Increment the org's recorded failure count by 1."""
        # Set default value to 0.
        self.cache_add(org, FAILURE_COUNT, value=0, timeout=RUNS_TIMEOUT)
        return self.cache_incr(org, FAILURE_COUNT)  # Increment value by 1.

    def fail_count_reset(self, org):
        """Reset the org's recorded failure count to 0."""
        self.cache_set(org, FAILURE_COUNT, value=0, timeout=RUNS_TIMEOUT)

    def lock_acquire(self, org):
        """Set a cache key that indicates the task is currently in progress.

        If the key is already set (task in progress), return False.
        """
        return self.cache_add(org, ORG_TASK_LOCK, value='true', timeout=LOCK_TIMEOUT)

    def lock_release(self, org):
        """Delete cache key that indicates that this task is in progress."""
        self.log_debug(org, "Starting to release lock.")
        self.cache_delete(org, ORG_TASK_LOCK)
        self.log_debug(org, "Released lock.")

    def run(self, org_pk):
        """Run the org_task with locks and logging."""

        org = apps.get_model('orgs', 'Org').objects.get(pk=org_pk)
        if self.lock_acquire(org):
            try:
                self.check_rate_limit(org)
            except ValueError as e:
                self.log_info(org, e.message)
                self.lock_release(org)
                return None

            try:
                self.log_info(org, "Starting task.")
                result = self.org_task(org)
            except Exception as e:
                fail_count = self.fail_count_incr(org)
                if isinstance(e, SoftTimeLimitExceeded):
                    msg = "Time limit exceeded (#{count})."
                    full_msg = self.log_error(org, msg, count=fail_count)
                    self.send_error_email(org, full_msg)
                    return None
                else:
                    msg = "Unknown failure (#{count})."
                    self.log_info(org, msg, count=fail_count)
                    raise
            else:
                self.fail_count_reset(org)
                self.log_info(org, "Finished task.")
                return result
            finally:
                self.lock_release(org)
        else:
            msg = "Skipping task because it is already running for this org."
            self.log_info(org, msg)
            return None

    def send_error_email(self, org, msg):
        # FIXME: Logging is not sending us regular logging error emails.
        self.log_debug(org, "Starting to send error email.")
        send_mail(
            subject="{}{}".format(settings.EMAIL_SUBJECT_PREFIX, msg),
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=dict(settings.ADMINS).values(),
            fail_silently=True)
        self.log_debug(org, "Finished sending error email.")

    def wrap_logger(self, level, org, msg, *args, **kwargs):
        kwargs.setdefault('org', org.name)
        msg = "{task} for {org}: " + msg
        return super(OrgTask, self).wrap_logger(level, msg, *args, **kwargs)


# from ucaptive.celery import app
# OrgTask = app.tasks.register(OrgTask())
