# -*- coding: utf-8 -*-
"""
lib/settings/config/base.py


"""
from __future__ import unicode_literals

import sys
import socket
import logging.config
from os import environ
from os.path import exists, join, dirname, abspath

from configurations import Configuration, values
from . import mixins as dj_mixins

_ = lambda x: x.encode('latin')


class DevSettingsMixin(object):
    """
    Quick-start development settings - unsuitable for production
    See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
    """

    # Turn off debug while imported by Celery with a workaround
    # See http://stackoverflow.com/a/4806384
    if "celery" in sys.argv[0]:
        DEBUG = False

    ############################################
    # settings for sending mail

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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

    @property
    def STATIC_ROOT(self):
        return join(self.WWW_DIR, 'public', 'static')

    ############################################
    # settings for logging

    @property
    def LOGGING(self):
        logging = super(StagingSettingsMixin, self).LOGGING
        logging['handlers']['django_log_file']['filename']= join(self.LOGGING_DIR, 'django.log')
        logging['handlers']['proj_log_file']['filename'] = join(self.LOGGING_DIR, 'project.log')
        return logging

    ############################################
    # Async tasking

    # Configure celery to use the django-celery backend.
    #CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'


class ProdSettingsMixin(object):
    """ Production settings """

    DEBUG = False
    STAGING = False
    HTTPS_ONLY = True


class AbstractBase(dj_mixins.AppsMixin, dj_mixins.MiddlewareMixin, dj_mixins.TemplatesMixin, dj_mixins.AuthURLMixin,
                   Configuration):
    """ 
    Basic Django configuration. 
    Expects env vars in 'settings/env/*.env' of current project.
    """

    # Pre-setup
    ############################################

    BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
    PROJECT_NAME = values.Value(str(BASE_DIR).rsplit("/", 1)[1], environ_prefix=None)
    SETTINGS_DIR = join(BASE_DIR, *environ['DJANGO_SETTINGS_MODULE'].split('.'))
    DOTENV = join(SETTINGS_DIR, 'env/%s.env' % socket.gethostname().split('.', 1)[0])

    # Define the Project's env vars
    ############################################
    LIBS_DIR = values.Value(join(str(BASE_DIR), 'lib'), environ_prefix='PROJECT')
    APPS_DIR = values.Value(join(str(BASE_DIR), 'apps'), environ_prefix='PROJECT')
    DATA_DIR = values.Value(join(dirname(str(BASE_DIR)), 'data'), environ_prefix='PROJECT')
    LOGGING_DIR = values.PathValue(join(BASE_DIR, 'logs'), checks_exists=True, environ_prefix='PROJECT')

    # Setup our python path
    sys.path.append(str(LIBS_DIR))
    sys.path.append(str(APPS_DIR))

    # Quick-start development settings - unsuitable for production
    ############################################

    SITE_ID = 1
    ADMINS = (
        ('EC.', 'ceduth@techoutlooks.com'),
    )
    # Got sent contact form input and BrokenLinkEmailsMIddleware
    MANAGERS = ADMINS + (
        ('Support Group', 'support@techoutlooks.com'),
    )

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True, environ_prefix=None)
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG, environ_prefix=None)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = values.Value(['localhost', '127.0.0.1'])
    INTERNAL_IPS = values.Value(['127.0.0.1'])

    # Application definition
    ############################################

    # replace django.contrib.auth.models.User by implementation
    # allowing to login via email address
    # AUTH_USER_MODEL = 'email_auth.User'

    # ROOT_URLCONF = values.Value('ucaptive.urls')
    # WSGI_APPLICATION = values.Value('ucaptive.wsgi.application')

    # eg.
    # Hack using .value to cast Configuration object to string
    DEFAULT_DATABASE_URL = 'sqlite:///db.sqlite3'
    DATABASES = values.DatabaseURLValue(DEFAULT_DATABASE_URL, alias='default').value
    # DATABASES['radius']  = values.DatabaseURLValue(DEFAULT_DATABASE_URL, alias='radius', environ_name='RADIUS_DATABASE_URL').value.get('radius')
    # DATABASE_ROUTERS = ['ucaptive.router.RadiusRouter']

    # INSTALLED APPS = ADMIN_APPS + DJANGO_APPS + DEV_APPS + DEFAULT_APPS + PROJECT_APPS +
    #                  CMS_APPS|BLOG_APPS|SEARCH_APPS|
    # Cf. settings/mixins/base.py

    # Static files management
    STATIC_URL = '/static/'

    #    STATICFILES_DIRS = (
    #        join(BASE_DIR, PROJECT_NAME, "static"),
    #    )

    @property
    def STATICFILES_DIRS(self):
        return (join(self.BASE_DIR, self.PROJECT_NAME, "static"),)

    # Absolute path to the directory that holds static files.
    STATIC_ROOT = join(BASE_DIR, 'staticfiles')

    # Absolute path to the directory that holds media.
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
    MEDIA_URL = "/media/"

    # settings for storing files and images
    ############################################
    THUMBNAIL_DEBUG = DEBUG
    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters'
    )
    # For easy_thumbnails to support retina displays (recent MacBooks, iOS)
    THUMBNAIL_HIGH_RESOLUTION = True

    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/
    ############################################

    LANGUAGE_CODE = 'en'

    # Local time zone for this installation.
    TIME_ZONE = values.Value('Africa/Conakry')
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGES = (
        ('fr', _('Français')),
        ('en', _('English')),
    )
    LOCALE_PATHS = (
        join(BASE_DIR, 'locale'),
    )

    FIXTURE_DIRS = (
        # join(dirname(SETTINGS_DIR), 'fixtures')
    )

    LOGIN_REDIRECT_URL = '/radmin/'
    LOGIN_URL = '/one_accounts/login/'

    # settings for logging
    ############################################
    # Reset logging first
    # http://www.caktusgroup.com/blog/2015/01/27/Django-Logging-Configuration-logging_config-default-settings-logger/
    LOGGING_CONFIG = None
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'django_log_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': join(str(LOGGING_DIR), 'django.log'),
                'formatter': 'verbose'
            },
            'proj_log_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': join(str(LOGGING_DIR), 'project.log'),
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['django_log_file'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'project': {
                'handlers': ['proj_log_file'],
                'level': 'DEBUG',
            },
            'django.security.DisallowedHost': {
                'handlers': ['console'],
            },
        }
    }
    if DEBUG:
        LOGGING['loggers']['django']['handlers'] = ['null']
    logging.config.dictConfig(LOGGING)

    class Meta:
        abstract = True
