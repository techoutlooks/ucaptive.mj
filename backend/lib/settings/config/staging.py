

class StagingSettingsMixin(object):
    """ Testing before going production """

    ############################################
    # Default environment

    # env
    STAGING = True
    DEBUG = values.Value(True)

    # dirs setting
    WWW_DIR = values.Value(environ_required=True)
    ALLOWED_HOSTS = values.Value(environ_required=True)
    LOGGING_ROOT = values.Value(environ_required=True)

    @property
    def STATIC_ROOT(self):
        return join(self.WWW_DIR, 'public', 'static')

    ############################################
    # settings for logging

    @property
    def LOGGING(self):
        logging = super(StagingSettingsMixin, self).LOGGING
        logging['handlers']['django_log_file']['filename']= join(self.LOGGING_ROOT, 'django.log')
        logging['handlers']['proj_log_file']['filename'] = join(self.LOGGING_ROOT, 'project.log')
        return logging

    ############################################
    # Async tasking

    # Configure celery to use the django-celery backend.
    #CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'