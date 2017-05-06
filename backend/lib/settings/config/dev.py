# coding=utf8

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


class DevSettingsMixin(object):

    # Local settings
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    INTERNAL_IPS = ['127.0.0.1']

    # Setting DEBUG sets TEMPLATE_DEBUG=True as well
    DEBUG = True
    THUMBNAIL_DEBUG = DEBUG

    # Turn off debug while imported by Celery with a workaround
    # See http://stackoverflow.com/a/4806384
    if "celery" in sys.argv[0]:
        DEBUG = False

    ############################################
    # settings for sending mail

    EMAIL_BACKEND = 'django.org.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@techoutlooks.com'
    #LOGGING['loggers']['django.security.DisallowedHost']['handlers'] =  ['null']

    STAGING = False
    HTTPS_ONLY = False

    @property
    def CSRF_COOKIE_SECURE(self):
        """ chained dynamic setting """
        return self.HTTPS_ONLY

    @property
    def SESSION_COOKIE_SECURE(self):
        """ chained dynamic setting """
        return self.HTTPS_ONLY
