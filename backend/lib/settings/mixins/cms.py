# settings/mixins/cms.py

from __future__ import unicode_literals

from os.path import join
from decimal import Decimal

from configurations import Configuration, values

_ = lambda x: x


class AbstractCMSMixin(object):
    """ DjangoCMS base settings """

    class Meta:
        abstract = True

    # Disable all cms features (djangocms_* apps) by default
    CMS_USE_BLOG = False
    CMS_USE_SHOP = False
    CMS_USE_SEARCH = True

    PARLER_DEFAULT_ACTIVATE = True
    PARLER_DEFAULT_LANGUAGE = 'en'
    PARLER_LANGUAGES = {
        1: (
            {'code': 'en'},
            {'code': 'fr'},
        ),
        'default': {
            'fallbacks': ['fr', 'en'],
        },
    }

    ############################################
    # settings for django-cms and its plugins

    CMS_MIDDLEWARE = (
        'cms.middleware.utils.ApphookReloadMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
    )  

    CMS_ADMIN_APPS = ('djangocms_admin_style',)

    CMS_APPS = [
        'cms',
        'menus',
        'djangocms_text_ckeditor',

        # plugins by contrib
        'djangocms_column',
        'djangocms_link',
        'cmsplugin_filer_file',
        'cmsplugin_filer_folder',
        'cmsplugin_filer_image',
        'cmsplugin_filer_utils',
        'djangocms_style',
        'djangocms_snippet',
        'djangocms_googlemap',
        'djangocms_video',

        # social plugins
        'connected_accounts',
        'connected_accounts.providers',
        'djangocms_twitter',
        'djangocms_instagram',
        'djangocms_vimeo',

        # plugins by me
        'plugins.components',
    ]

    BLOG_APPS = [

        # cms requires
        'filer',
        'easy_thumbnails',
        'aldryn_apphooks_config',
        'cmsplugin_filer_image',
        'parler',
        'taggit',
        'taggit_autosuggest',
        'meta',
        'djangocms_blog',
    ]

    SHOP_APPS = [
        # 'django.contrib.auth',
        # 'email_auth',
        'polymorphic',
        # 'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        # 'django.contrib.sites',
        # 'djangocms_admin_style', the default style in Django-1.9 is good enough
        # 'django.contrib.admin',
        # 'django.contrib.staticfiles',
        # 'django.contrib.sitemaps',

        # 'djangocms_text_ckeditor',
        'django_select2',
        'cmsplugin_cascade',
        'cmsplugin_cascade.clipboard',
        'cmsplugin_cascade.sharable',
        'cmsplugin_cascade.extra_fields',
        'cmsplugin_cascade.segmentation',
        'cms_bootstrap3',
        # 'cms',
        # 'menus',
        # 'treebeard',
        'compressor',
        'sekizai',

        'adminsortable2',
        'rest_framework',
        'rest_framework.authtoken',
        'rest_auth',
        'django_fsm',
        'fsm_admin',
        'djng',

        'sass_processor',
        'django_filters',
        # 'filer',
        # 'easy_thumbnails',
        'easy_thumbnails.optimize',
        'parler',
        'post_office',
        'shop',
        'shop_stripe',

        'apps.shopext',
    ]

    SEARCH_APPS = [
        'haystack',
    ]

    @property
    def INSTALLED_APPS(self):
        self.ADMIN_APPS = self.CMS_ADMIN_APPS
        apps = list(super(AbstractCMSMixin, self).INSTALLED_APPS) + self.CMS_APPS

        def get_apps(feature):
            return {
                'CMS_USE_BLOG': self.BLOG_APPS,
                'CMS_USE_SHOP': self.SHOP_APPS,
                'CMS_USE_SEARCH': self.SEARCH_APPS,
            }.get('CMS_USE_%s' % feature)

        for feature in ['BLOG', 'SHOP', 'SEARCH']:
            if getattr(self, 'CMS_USE_%s' % feature, False):
                apps += [app for app in get_apps(feature) if app not in apps]
        return apps

    # TEMPLATES

    CMS_CONTEXT_PROCESSORS = [
        'cms.context_processors.cms_settings',
    ]
    BLOG_CONTEXT_PROCESSORS = []
    SHOP_CONTEXT_PROCESSORS = [
        'shop.context_processors.customer',
        'shop.context_processors.version',
        'shop_stripe.context_processors.public_keys',
    ]
    SEARCH_CONTEXT_PROCESSORS = []

    @property
    def TEMPLATES(self):

        templates = list(super(AbstractCMSMixin, self).TEMPLATES)
        options = templates[0].get('OPTIONS')
        cms_context_processors = options.get('context_processors') + self.CMS_CONTEXT_PROCESSORS

        def get_processors(cms_feature):
            return {
                'CMS_USE_BLOG': self.BLOG_CONTEXT_PROCESSORS,
                'CMS_USE_SHOP': self.SHOP_CONTEXT_PROCESSORS,
                'CMS_USE_SEARCH': self.SEARCH_CONTEXT_PROCESSORS,
            }.get('CMS_USE_%s' % cms_feature)

        for cms_feature in ['BLOG', 'SHOP', 'SEARCH']:
            if getattr(self, 'CMS_USE_%s' % cms_feature, False):
                cms_context_processors += [p for p in get_processors(cms_feature) if p not in cms_context_processors]

        options.update({"context_processors": cms_context_processors})

        return templates

    @property
    def CMS_LANGUAGES(self):
        if super(AbstractCMSMixin, self).USE_I18N:
            return {
                'default': {
                    'fallbacks': ['en', 'fr'],
                    'redirect_on_fallback': True,
                    'public': True,
                    'hide_untranslated': False,
                },
                1: ({
                        'public': True,
                        'code': 'en',
                        'hide_untranslated': False,
                        'name': 'English',
                        'redirect_on_fallback': True,
                    }, {
                        'public': True,
                        'code': 'fr',
                        'hide_untranslated': False,
                        'name': 'French',
                        'redirect_on_fallback': True,
                    },)
            }

    # A list of templates you can select for a page.
    # http://docs.django-cms.org/en/release-3.4.x/reference/configuration.html?highlight=cms_templates
    CMS_TEMPLATES = (
        ('base.html', 'Base'),
        ('home.html', 'Home'),
        ('blog.html', 'Blog'),
    )

    CMS_PERMISSION = True
    CMS_PLACEHOLDER_CONF = {}


class CMSBlogMixin(AbstractCMSMixin):

    CMS_USE_BLOG = True

    ############################################
    # djangocms-blog settings

    # Template override from our 'blogext' app
    BLOG_TEMPLATES = (
        ('blogext/plugins/latest_entries.html', _('Default')),
        ('blogext/plugins/latest_entries_featured.html', _('Featured')),
        ('blogext/plugins/latest_entries_footer.html', _('Footer')),
    )

    # http://djangocms-blog.readthedocs.io/en/latest/installation.html#minimal-configuration
    META_SITE_PROTOCOL = 'http'
    META_USE_SITES = True

    BLOG_POSTS_LIST_TRUNCWORDS_COUNT = 10

    ############################################
    # Plugins definition
    # TODO: Move to some place more appropriate

    # Configure parler according your languages:
    # PARLER_LANGUAGES =

    # Enable Twitter as a provider for django-connected
    # You can register an app on Twitter via https://apps.twitter.com/app/new
    # pip install djangocms-twitter2
    CONNECTED_ACCOUNTS_TWITTER_CONSUMER_KEY = values.Value()
    CONNECTED_ACCOUNTS_TWITTER_CONSUMER_SECRET = values.Value()
    DJANGOCMS_TWITTER_TEMPLATES = (
        ('djangocms_twitter/default.html', _('Default')),
        ('djangocms_twitter/sidebar.html', _('Sidebar')),
    )

    # Enable Instagram as a provider for django-connected
    # Register your OAuth app here: https://instagram.com/developer/clients/register/
    CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_KEY = values.Value()
    CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_SECRET = values.Value()
    DJANGOCMS_INSTAGRAM_TEMPLATES = (
        ('djangocms_instagram/default.html', _('Default')),
        ('djangocms_instagram/footer.html', _('Footer')),
    )

    # Vimeo plugin settings
    CMS_VIMEO_TEMPLATES = (
        ('djangocms_vimeo/default.html', _('Default')),
        ('djangocms_vimeo/video.html', _('Video')),
    )

    # Google Maps Plugin settings
    DJANGOCMS_GOOGLEMAP_API_KEY = values.Value()
    DJANGOCMS_GOOGLEMAP_TEMPLATES = [
        ('djangocms_googlemap/googlemap.html', _('Default')),
        ('djangocms_googlemap/googlemap_footer.html', _('Footer')),
    ]


class CMSShopMixin(AbstractCMSMixin):
    """
    Django settings for Django SHOP.
    http://django-shop.readthedocs.io/en/latest/index.html

    """
    CMS_USE_SHOP = True

    SHOP_APP_LABEL = 'shopext'

    # DJANGO_SHOP_MODEL_VARIANT = simple|i18n|polymorphic
    # http://django-shop.readthedocs.io/en/latest/tutorial/polymorphic-product.html
    SHOP_MODEL_VARIANT = values.Value('polymorphic')

    if SHOP_MODEL_VARIANT not in ('simple', 'i18n', 'polymorphic',):
        raise Exception("Environment DJANGO_SHOP_MODEL_VARIANT has an invalid value `{}`"
                                   .format(SHOP_MODEL_VARIANT))

    ############################################
    # Application definition

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    @property
    def MIDDLEWARE_CLASSES(self):
        dj_classes = super(CMSShopMixin, self).DJANGO_MIDDLEWARE + ('django.middleware.gzip.GZipMiddleware',)
        cms_classes = self.CMS_MIDDLEWARE + ('cms.middleware.toolbar.ToolbarMiddleware',)
        out_classes = \
            ('djng.middleware.AngularUrlMiddleware',) + \
            dj_classes + cms_classes + \
            (  # 'django.middleware.cache.UpdateCacheMiddleware',
                'shop.middleware.CustomerMiddleware',
                # 'django.middleware.cache.FetchFromCacheMiddleware',
            )
        if self.DEBUG:
            out_classes += self.DEBUG_MIDDLEWARE
        return out_classes

    MIGRATION_MODULES = {
        'shopext': 'apps.shopext.migrations.{}'.format(SHOP_MODEL_VARIANT)
    }

    # Internationalization
    # https://docs.djangoproject.com/en/stable/topics/i18n/
    if SHOP_MODEL_VARIANT in ('i18n', 'polymorphic'):
        USE_I18N = True
    else:
        USE_I18N = False


    USE_X_FORWARDED_HOST = True

    @property
    def STATICFILES_FINDERS(self):
        return (
            'apps.shopext.finders.FileSystemFinder',       # or 'django.contrib.staticfiles.finders.FileSystemFinder',
            'apps.shopext.finders.AppDirectoriesFinder',   # or 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'sass_processor.finders.CssFinder',
            'compressor.finders.CompressorFinder',
        )

    @property
    def STATICFILES_DIRS(self):
        return super(CMSShopMixin, self).STATICFILES_DIRS + (
            # os.path.join(BASE_DIR, 'static'),
            ('bower_components', join(self.BASE_DIR, 'staticfiles', 'bower_components')),
            ('node_modules', join(self.BASE_DIR, 'staticfiles', 'node_modules')),
        )

    # URL prefix for admin media -- CSS, JavaScript and images.
    # Make sure to use a trailing slash.
    # Deprecated
    # ADMIN_MEDIA_PREFIX = '/static/admin/'

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': True,
    #     'filters': {
    #         'require_debug_false': {
    #             '()': 'django.utils.log.RequireDebugFalse',
    #         }
    #     },
    #     'formatters': {
    #         'simple': {
    #             'format': '[%(asctime)s %(module)s] %(levelname)s: %(message)s'
    #         },
    #     },
    #     'handlers': {
    #         'console': {
    #             'level': 'INFO',
    #             'class': 'logging.StreamHandler',
    #             'formatter': 'simple',
    #         },
    #     },
    #     'loggers': {
    #         'django': {
    #             'handlers': ['console'],
    #             'level': 'INFO',
    #             'propagate': True,
    #         },
    #         'post_office': {
    #             'handlers': ['console'],
    #             'level': 'WARNING',
    #             'propagate': True,
    #         },
    #     },
    # }

    SILENCED_SYSTEM_CHECKS = ('auth.W004')

    ############################################
    # settings for sending mail

    # EMAIL_HOST = 'smtp.example.com'
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = 'no-reply@example.com'
    # EMAIL_HOST_PASSWORD = 'smtp-secret-password'
    # EMAIL_USE_TLS = True
    # DEFAULT_FROM_EMAIL = 'My Shop <no-reply@example.com>'
    # EMAIL_REPLY_TO = 'info@example.com'
    # EMAIL_BACKEND = 'post_office.EmailBackend'

    ############################################
    # settings for third party Django apps

    @property
    def NODE_MODULES_URL(self):
        return self.STATIC_URL + 'node_modules/'

    @property
    def SASS_PROCESSOR_INCLUDE_DIRS(self):
        return (join(self.BASE_DIR, 'staticfiles', 'node_modules'),)

    COERCE_DECIMAL_TO_STRING = True

    FSM_ADMIN_FORCE_PERMIT = True

    ROBOTS_META_TAGS = ('noindex', 'nofollow')

    ############################################
    # settings for django-restframework and plugins

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'shop.rest.money.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',  # can be disabled for production environments
        ),
        # 'DEFAULT_AUTHENTICATION_CLASSES': (
        #   'rest_framework.authentication.TokenAuthentication',
        # ),
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 12,
    }

    SERIALIZATION_MODULES = {'json': str('shop.money.serializers')}

    ############################################
    # settings for storing session data

    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_SAVE_EVERY_REQUEST = True

    ############################################
    # settings for storing files and images

    FILER_ADMIN_ICON_SIZES = ('16', '32', '48', '80', '128')

    FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

    FILER_DUMP_PAYLOAD = False

    FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

    THUMBNAIL_HIGH_RESOLUTION = False

    THUMBNAIL_OPTIMIZE_COMMAND = {
        'gif': '/usr/bin/optipng {filename}',
        'jpeg': '/usr/bin/jpegoptim {filename}',
        'png': '/usr/bin/optipng {filename}'
    }

    THUMBNAIL_PRESERVE_EXTENSIONS = True


    ############################################
    # settings for django-cms and its plugins

    @property
    def CMS_TEMPLATES(self):
        templates = [('shopext/pages/default.html', _("Default Page")),]
        for cms_tpl in super(CMSShopMixin, self).CMS_TEMPLATES:
            templates.append(cms_tpl)
        return templates

    CMS_CACHE_DURATIONS = {
        'content': 600,
        'menus': 3600,
        'permissions': 86400,
    }

    CMS_PERMISSION = False

    CACSCADE_WORKAREA_GLOSSARY = {
        'breakpoints': ['xs', 'sm', 'md', 'lg'],
        'container_max_widths': {'xs': 750, 'sm': 750, 'md': 970, 'lg': 1170},
        'fluid': False,
        'media_queries': {
            'xs': ['(max-width: 768px)'],
            'sm': ['(min-width: 768px)', '(max-width: 992px)'],
            'md': ['(min-width: 992px)', '(max-width: 1200px)'],
            'lg': ['(min-width: 1200px)'],
        },
    }

    CMS_PLACEHOLDER_CONF = {
        'Breadcrumb': {
            'plugins': ['BreadcrumbPlugin'],
            'glossary': CACSCADE_WORKAREA_GLOSSARY,
        },
        'Commodity Details': {
            'plugins': ['BootstrapRowPlugin', 'TextPlugin', 'ImagePlugin', 'PicturePlugin'],
            'text_only_plugins': ['TextLinkPlugin'],
            'parent_classes': {'BootstrapRowPlugin': []},
            'require_parent': False,
            'glossary': CACSCADE_WORKAREA_GLOSSARY,
        },
    }

    CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.segmentation', 'cmsplugin_cascade.generic',
                                 'cmsplugin_cascade.link', 'shop.cascade', 'cmsplugin_cascade.bootstrap3',)

    CMSPLUGIN_CASCADE = {
        'dependencies': {
            'shop/js/admin/shoplinkplugin.js': 'cascade/js/admin/linkpluginbase.js',
        },
        'alien_plugins': ('TextPlugin', 'TextLinkPlugin',),
        'bootstrap3': {
            'template_basedir': 'angular-ui',
        },
        'plugins_with_extra_fields': (
            'BootstrapButtonPlugin',
            'BootstrapRowPlugin',
            'SimpleWrapperPlugin',
            'HorizontalRulePlugin',
            'ExtraAnnotationFormPlugin',
            'ShopProceedButton',
        ),
        'segmentation_mixins': (
            ('shop.cascade.segmentation.EmulateCustomerModelMixin',
             'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
        ),
    }

    CMSPLUGIN_CASCADE_LINKPLUGIN_CLASSES = (
        'shop.cascade.plugin_base.CatalogLinkPluginBase',
        'cmsplugin_cascade.link.plugin_base.LinkElementMixin',
        'shop.cascade.plugin_base.CatalogLinkForm',
    )

    CKEDITOR_SETTINGS = {
        'language': '{{ language }}',
        'skin': 'moono',
        'toolbar': 'CMS',
        'toolbar_HTMLField': [
            ['Undo', 'Redo'],
            ['cmsplugins', '-', 'ShowBlocks'],
            ['Format', 'Styles'],
            ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
            ['Maximize', ''],
            '/',
            ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['HorizontalRule'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
            ['Source']
        ],
    }

    SELECT2_CSS = 'bower_components/select2/dist/css/select2.min.css'
    SELECT2_JS = 'bower_components/select2/dist/js/select2.min.js'


    ############################################
    # settings for django-shop and its plugins

    SHOP_VALUE_ADDED_TAX = Decimal(19)
    SHOP_DEFAULT_CURRENCY = 'EUR'
    SHOP_CART_MODIFIERS = (
        'apps.shopext.polymorphic_modifiers.ShopExtCartModifier' if SHOP_MODEL_VARIANT == 'polymorphic'
        else 'shop.modifiers.defaults.DefaultCartModifier',
        'shop.modifiers.taxes.CartExcludedTaxModifier',
        'apps.shopext.modifiers.PostalShippingModifier',
        'apps.shopext.modifiers.CustomerPickupModifier',
        'apps.shopext.modifiers.StripePaymentModifier',
        'shop.modifiers.defaults.PayInAdvanceModifier',
    )
    SHOP_EDITCART_NG_MODEL_OPTIONS = "{updateOn: 'default blur', debounce: {'default': 2500, 'blur': 0}}"

    SHOP_ORDER_WORKFLOWS = (
        'shop.payment.defaults.PayInAdvanceWorkflowMixin',
        'shop.shipping.delivery.PartialDeliveryWorkflowMixin' if SHOP_MODEL_VARIANT == 'polymorphic'
        else 'shop.shipping.defaults.CommissionGoodsWorkflowMixin',
        'shop_stripe.payment.OrderWorkflowMixin',
    )

    SHOP_STRIPE = {
        'PUBKEY': 'pk_test_stripe_secret',
        'APIKEY': 'sk_test_stripe_secret',
        'PURCHASE_DESCRIPTION': _("Thanks for purchasing at shopext"),
    }

    # merge settings with non-public credentioals in private_settings
    for priv_attr in ('DATABASES', 'SECRET_KEY', 'SHOP_STRIPE', 'EMAIL_HOST', 'EMAIL_PORT',
                      'EMAIL_HOST_USER', 'DEFAULT_FROM_EMAIL', 'EMAIL_HOST_PASSWORD', 'EMAIL_USE_TLS',
                      'EMAIL_REPLY_TO', 'EMAIL_BACKEND'):
        try:
            from . import private_settings
            vars()[priv_attr].update(getattr(private_settings, priv_attr))
        except AttributeError:
            continue
        except KeyError:
            vars()[priv_attr] = getattr(private_settings, priv_attr)
        except ImportError:
            break
