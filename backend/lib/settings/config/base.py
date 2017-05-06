"""
lib/settings/config/base.py


"""


class AbstractBase(AppsMixin, MiddlewareMixin, TemplatesMixin, AuthURLMixin, Configuration):
    """
    Basic Django configuration

    """
    # Define the Project's directories
    ############################################
    root = environ.Path(__file__)
    BASE_DIR = env('BASE_DIR', default=(root-3)())
    APPS_DIR = join(BASE_DIR, 'apps')
    LIBS_DIR = join(BASE_DIR, 'lib')
    SETTINGS_DIR = join(BASE_DIR, *env('DJANGO_SETTINGS_MODULE').split('.'))
    DATA_DIR = join(BASE_DIR, 'data')
    PROJECT_NAME = BASE_DIR.rsplit("/", 1)[1]

    # Setup our python path
    sys.path.append(APPS_DIR)
    sys.path.append(LIBS_DIR)

    # Quick-start development settings - unsuitable for production
    ############################################

    SITE_ID = 1
    ADMINS = (
        ('EC.', 'ceduth@techoutlooks.com' ),
    )
    # Got sent contact form input and BrokenLinkEmailsMIddleware
    MANAGERS = ADMINS + (
        ('Support Group', 'support@techoutlooks.com'),
    )

    # Collected from settings/env/*.env

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.Value()

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
    STATICFILES_DIRS = (
        join(BASE_DIR, PROJECT_NAME.rsplit('.', 1)[0], "static"),
    )

    # Absolute path to the directory that holds static files.
    STATIC_ROOT = join(BASE_DIR, 'staticfiles')

    # Absolute path to the directory that holds media.
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
    MEDIA_URL = "/media/"

    # settings for storing files and images
    ############################################

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters'
    )

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
        ('fr', _('Français'.decode(encoding='latin'))),
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
    LOGGING_ROOT = join(BASE_DIR, 'logs')
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
                'class':'logging.NullHandler',
                },
            'django_log_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': join(LOGGING_ROOT, 'django.log'),
                'formatter': 'verbose'
            },
            'proj_log_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': join(LOGGING_ROOT, 'project.log'),
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


    ############################################
    # For loading additional configuration
    # todo: must load from importing project, not lib/settings/env/*, or create python package from lib.settings ?

    # Use 12factor inspired environment variables or from a file
    # Ideally move env file outside the git repo
    env_file = join(SETTINGS_DIR, 'env/%s.env' % socket.gethostname().split('.', 1)[0])
    if exists(env_file):
        environ.Env.read_env(str(env_file))
        
    class Meta:
        abstract = True
