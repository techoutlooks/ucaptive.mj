# -*- coding: utf-8 -*-
# settings/config/base.py

from configurations import values
import dj_database_url

from os.path import exists, join, dirname, abspath, pardir
from lib.settings.conf import AbstractBaseSettings
from lib.settings.mixins import CompressorSettingsMixin
from lib.djros.settings import DjROSSettingsMixin
from apps.orgs.settings import OrgTaskSettingsMixin
from apps.cities.settings import CitiesSettingsMixin
from ..mixins import DataImportersettingsMixin


class BaseSettings(DjROSSettingsMixin, CompressorSettingsMixin, OrgTaskSettingsMixin, DataImportersettingsMixin, CitiesSettingsMixin, AbstractBaseSettings):
    """ Basic Django configuration """

    ############################################
    # Project settings
    DEBUG = AbstractBaseSettings.DEBUG
    MANAGERS = AbstractBaseSettings.ADMINS + (
        ('Support Group', 'support@techoutlooks.com'),
    )

    ############################################
    # Application definition

    # replace django.contrib.auth.models.User by implementation
    # allowing to login via phone number. eg:
    AUTH_USER_MODEL = 'accounts.Reporter'

    ROOT_URLCONF = values.Value('ucaptive.urls')
    WSGI_APPLICATION = values.Value('ucaptive.wsgi.application')

    # Database routing
    # eg. Radius, Ureporters, Staff/Admins, Radius databases
    DATABASE_ROUTERS = ['ucaptive.router.RadiusRouter']
    DEFAULT_DATABASE_URL = 'sqlite:///db.sqlite3'

    def DATABASES(self):
        return {
            "default": dj_database_url.config(env='DATABASE_URL', default=self.DEFAULT_DATABASE_URL),
            "radius": dj_database_url.config(env='RADIUS_DATABASE_URL', default=self.DEFAULT_DATABASE_URL),
        }

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
        # 'smart_selects',                    # provides ChainedForeignKey model used in cities app

        # django-filer dependencies below
        'easy_thumbnails',
        'filer',
        'mptt',
        'sekizai',
        'crispy_forms',

        # todo: delete tastypie when DRF3 code for freeradius.api.* is clean.
        # 'tastypie',

        'corsheaders',
        'rest_framework',                   # DRF3
        'rest_framework_api_key',
        'djng',                             # django-angular

        # TODO: make package
        # my libs
        'one_auth',
        'one_accounts',                     #
        'contacts',                         # django-contacts
        'data_importer',                    # xlsx, csv to models

        'djra.freeradius.apps.FreeRadiusConfig',
        'djra.radmin',
        'djra.reports',
        'djros',
    )

    PROJECT_APPS = (
        'apps.accounts',
        'apps.cities',
        'apps.layout',
        'apps.orgs',
        'ucaptive',
    )

    STATIC_URL = '/static/'

    @property
    def STATICFILES_DIRS(self):
        # bower_components: jQuery, node_modules: nodejs
        COMPONENTS_DIR = join(dirname(self.BASE_DIR), 'components')
        return super(BaseSettings, self).STATICFILES_DIRS + (
            ('bower_components', join(COMPONENTS_DIR, 'bower_components')),
            ('node_modules', join(COMPONENTS_DIR, 'node_modules')),
            ('vendor', join(COMPONENTS_DIR, 'vendor')),
            ('gmaps', join(dirname(self.BASE_DIR), 'data', 'gmaps'))
        )

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
            'one_accounts.api.permissions.IsOneUserAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
    }

    # Adding CORS (Cross-Origin Resource Sharing) headers to responses.
    # Cf. https://github.com/ottoyiu/django-cors-headers/

    CORS_ORIGIN_WHITELIST = (
        'localhost'
        'ucaptive.cloud.com.gn:8000',
        'jeunesse.cloud.com.gn:8000',
        'ucaptive.cloud.com.gn',
        'jeunesse.cloud.com.gn',
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
        'one-token',
        'api-key',
    )

    # CORS_URLS_REGEX = r'^/api/.*$'

    # override if debug
    CORS_ALLOW_CREDENTIALS = CORS_ORIGIN_ALLOW_ALL = DEBUG


    ############################################
    # https://github.com/stefanfoulis/django-phonenumber-field

    PHONENUMBER_DB_FORMAT = 'NATIONAL'
    PHONENUMBER_DEFAULT_REGION = 'GN'

    ############################################
    # Settings
    # Cf for djra.freeradius
    DJRA_DEFAULT_GROUP = 'ureporters'


    ############################################
    # rest_framework_api_key
    DRF3_APIKEY_MODEL = 'orgs.OrgApiKeyToken'
