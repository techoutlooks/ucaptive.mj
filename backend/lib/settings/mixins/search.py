# coding=utf8
# settings/mixins/search.py

from __future__ import unicode_literals


class SearchMixin(object):
    """
    Settings for full index text search (Haystack)

    Comes after AbstractCMSMixin
    """

    CMS_USE_BLOG = True

    @property
    def SHOP_MODEL_VARIANT(self):
        return super(SearchMixin, self).SHOP_MODEL_VARIANT

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://localhost:9200/',
            'INDEX_NAME': 'shopext-en',
        },
    }

    if SHOP_MODEL_VARIANT in ('i18n', 'polymorphic'):
        HAYSTACK_CONNECTIONS['fr'] = {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://localhost:9200/',
            'INDEX_NAME': 'shopext-fr',
        }

    HAYSTACK_ROUTERS = ('shop.search.routers.LanguageRouter',)
