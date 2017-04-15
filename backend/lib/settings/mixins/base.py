# settings/mixins/base.py

from __future__ import unicode_literals

from os.path import join, dirname
# from django.core.urlresolvers import reverse_lazy




class MiddlewareMixin(object):
    """ Django settings.MIDDLEWARE_CLASSES as a Mixin """

    DJANGO_MIDDLEWARE = (
        #'django.middleware.common.BrokenLinkEmailsMIddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    )

    DEBUG_MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEFAULT_MIDDLEWARE = ()
    PROJECT_MIDDLEWARE = ()

    @property
    def MIDDLEWARE_CLASSES(self):
        out_classes = self.DEFAULT_MIDDLEWARE + self.DJANGO_MIDDLEWARE + self.PROJECT_MIDDLEWARE
        if self.DEBUG:
            out_classes += self.DEBUG_MIDDLEWARE
        return list(out_classes)


class AppsMixin(object):
    """
    Django settings.INSTALLED_APPS as a Mixin

    ADMIN_APPS:       Extend django.contrib.admin.
    DEV_APPS:         Not for production usage.
    DEFAULT_APPS:     Well-known, usually extensively used apps. Also installed related context_processors.
    PROJECT_APPS:     Custom (current project)'s apps.
    """

    DJANGO_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.sites',	
        'django.contrib.sitemaps',
        'django.contrib.staticfiles',
        'django.contrib.messages',
    )

    ADMIN_APPS = ()
    DEV_APPS = ('django.contrib.admindocs', 'debug_toolbar.apps.DebugToolbarConfig', 'django_extensions')
    DEFAULT_APPS = ()
    PROJECT_APPS = ()

    @property
    def INSTALLED_APPS(self):
        """ Control application ordering dynamically """
        out_apps = self.ADMIN_APPS + self.DEFAULT_APPS + self.DJANGO_APPS
        if self.DEBUG:
            out_apps += self.DEV_APPS
        return out_apps + self.PROJECT_APPS


class AuthURLMixin(object):

    # todo: buggy/bad practice to call django from django (circular redundancy). fails django-compressor.
    # LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
    # LOGIN_URL = reverse_lazy("one_accounts:login")
    # LOGOUT_URL = '/auth/logout/'
    pass


class TemplatesMixin(object):
    """ Django settings.TEMPLATES as a Mixin """

    @property
    def TEMPLATES(self):

        templates = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    join(self.BASE_DIR, 'theme', 'templates'),
                    join(dirname(self.SETTINGS_DIR), 'templates'),
                ],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': filter(None, [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'django.core.context_processors.i18n',
                        'django.core.context_processors.debug',
                        'django.core.context_processors.request',
                        'django.core.context_processors.media',
                        'django.core.context_processors.csrf',
                        'django.core.context_processors.tz',
                        'django.core.context_processors.static',
                        'sekizai.context_processors.sekizai' if 'sekizai' in self.INSTALLED_APPS else None
                    ]),
                },
            },
        ]

        # Cache the templates in memory for speed-up
        cached_loaders = [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ]

        if not self.DEBUG:
            # Production settings
            templates[0]['OPTIONS'].update({"loaders": cached_loaders})
            templates[0]['OPTIONS'].update({'debug': self.DEBUG})
            templates[0].update({"APP_DIRS": False})

        return templates


class EmailMixin(object):
    """
    Django settings for sending email.

    """

    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST = 'mail.techoutlooks.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'noreply@techoutlooks.com'
    EMAIL_HOST_PASSWORD = 'techu0910!'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        return '[TechOutlooks {}] '.format(self.PROJECT_NAME)


class CrispyFormsMixin(object):
    """ django-crispy-forms specific settings """

    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    # For Bootstrap 3, change error alert to 'danger'

    @property
    def CRISPY_FAIL_SILENTLY(self):
        return not self.DEBUG




