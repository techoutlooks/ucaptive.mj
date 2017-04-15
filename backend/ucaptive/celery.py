from __future__ import absolute_import

import os
import sys
import configurations
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ucaptive.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

# suport for django-configurations
# only calling django's setup() function for Celery processes
# avoids circular redundancy errors (calling anything django from settings).
# eg., fails django-compressor.
if sys.argv[0].endswith('celery'):
    configurations.setup()  # calls django.setup() ...

from django.conf import settings  # noqa

app = Celery('ucaptive')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
