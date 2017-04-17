# -*- coding: utf-8 -*-
# settings/config/base.py

from os.path import exists, join, dirname, abspath, pardir

from configurations import values
from lib.settings.conf import AbstractBase
from lib.settings.mixins import CompressorMixin
from ..mixins import CitiesMixin, DataImporterMixin, CeleryMixin
from configurations import values


class Base(CompressorMixin, CeleryMixin, DataImporterMixin, CitiesMixin, AbstractBase):
    """ Basic Django configuration """

    ############################################
    # Project settings
    DEBUG = AbstractBase.DEBUG
    MANAGERS = AbstractBase.ADMINS + (
        ('Support Group', 'support@techoutlooks.com'),
    )

    ############################################
    # Application definition

    # replace django.contrib.auth.models.User by implementation
    # allowing to login via phone number. eg:
    AUTH_USER_MODEL = 'accounts.Reporter'

    ROOT_URLCONF = values.Value('ucaptive.urls')
    WSGI_APPLICATION = values.Value('ucaptive.wsgi.application')

    # Hack using .value to cast Configuration object to string
    DEFAULT_DATABASE_URL = 'sqlite:///db.sqlite3'
    DATABASES = values.DatabaseURLValue(DEFAULT_DATABASE_URL, alias='default').value
    DATABASES['radius'] = values.DatabaseURLValue(DEFAULT_DATABASE_URL, alias='radius',
                                                   environ_name='RADIUS_DATABASE_URL').value.get('radius')

    # Database routing
    # eg. Radius, Ureporters, Staff/Admins databases
    DATABASE_ROUTERS = ['ucaptive.router.RadiusRouter']

    # MiddlewareMixin
    # Cf. backend/lib/settings/mixins/base.py
    # MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE + DJANGO_MIDDLEWARE + PROJECT_MIDDLEWARE
    DEFAULT_MIDDLEWARE = (
        'corsheaders.middleware.CorsMiddleware',
        # 'lib.middleware.ajax.AjaxMessaging',
    )

    # AppsMixin.DEFAULT_APPS (Well-known, extensively used apps)
    # Eventual context processors for DEFAULT apps already
    # Cf. backend/lib/settings/mixins/base.py
    # INSTALLED APPS = PROJECT_APPS|CMS_APPS|BLOG_APPS|SEARCH_APPS|
    DEFAULT_APPS = (
        'paging',
        'test_utils',
        'phonenumber_field',
        'smart_selects',                    # provides ChainedForeignKey model used in cities app

        # django-filer dependencies below
        'easy_thumbnails',
        'filer',
        'mptt',
        'sekizai',
        'crispy_forms',

        # todo: sanitize, use either of tastypie (freeradius) or  djangorestframework
        'tastypie',

        'corsheaders',
        'rest_framework',
        'djng',                             # django-angular

        'one_auth',
        'one_accounts',                     #
        'data_importer',                    # xlsx, csv to models
    )

    PROJECT_APPS = (
        'ucaptive',
        'djra.freeradius.apps.FreeRadiusConfig',
        'djra.radmin',
        'djra.reports',
        'accounts',
        'cities',
        'layout',
    )

    STATIC_URL = '/static/'

    @property
    def STATICFILES_DIRS(self):
        """
        bower_components: jQuery
        node_modules: nodejs
        """
#        print "STATICFILES_DIRS  = %s" % super(Base, self).STATICFILES_DIRS
        return super(Base, self).STATICFILES_DIRS + (
            ('bower_components', join(self.BASE_DIR, 'components', 'bower_components')),
            ('node_modules', join(self.BASE_DIR, 'components', 'node_modules')),
            ('vendor', join(self.BASE_DIR, 'components', 'vendor')),
        )

    ############################################
    # Settings for storing files and images

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters'
    )

    # For easy_thumbnails to support retina displays (recent MacBooks, iOS) add to settings.py
    THUMBNAIL_HIGH_RESOLUTION = True

    #IP_DB_FILE = '/some/path/to/ipdb.dat'

    ############################################
    # django-registration settings
    ACCOUNT_ACTIVATION_DAYS = 2

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.MultiPartParser',
            'rest_framework.parsers.FileUploadParser',
        ),
        'EXCEPTION_HANDLER': 'lib.restutils.custom_exception_handler',
        'DEFAULT_PERMISSION_CLASSES': (
            'one_accounts.permissions.IsOneUserAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
    }

    # Adding CORS (Cross-Origin Resource Sharing) headers to responses.
    # Cf. https://github.com/ottoyiu/django-cors-headers/
    CORS_ALLOW_CREDENTIALS = CORS_ORIGIN_ALLOW_ALL = DEBUG

    # todo if debug
    CORS_ORIGIN_WHITELIST = (
        'localhost'
    )

    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS'
    )

    CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'one-token'
    )

    # CORS_URLS_REGEX = r'^/api/.*$'

    ############################################
    # https://github.com/stefanfoulis/django-phonenumber-field
    PHONENUMBER_DB_FORMAT = 'NATIONAL'
    PHONENUMBER_DEFAULT_REGION = 'GN'
