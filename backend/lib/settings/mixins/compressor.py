# -*- coding: utf-8 -*-
"""
Enables support for SCSS and ES6 in Django.
https://github.com/kottenator/django-compressor-toolkit

The add-on does:
    SCSS → ( node-sass + Autoprefixer ) → CSS.
    ES6 → ( Browserify + Babelify ) → ES5.

Requisites:
    (scss) npm install node-sass postcss-cli autoprefixer

"""
from os.path import join


class CompressorMixin(object):

    ############################################
    # Requisites

    @property
    def INSTALLED_APPS(self):
         apps = super(CompressorMixin, self).INSTALLED_APPS
         apps += ('compressor', 'compressor_toolkit',)
         return apps

    @property
    def STATICFILES_FINDERS(self):
        finders = super(CompressorMixin, self).STATICFILES_FINDERS
        finders += ('compressor.finders.CompressorFinder',)
        return finders

    # @property
    # def COMPRESS_ROOT(self):
    #     return join(self.BASE_DIR, 'dist')

#    @property
#    def COMPRESS_URL(self):
#        return self.STATIC_URL

    # COMPRESS_DEBUG_TOGGLE = None
    # COMPRESS_ENABLED = True

    ############################################
    # ES6 Plugin. Default:

    @property
    def COMPRESS_BROWSERIFY_BIN(self):
        return join(self.BASE_DIR, 'components', 'node_modules/.bin/browserify')

    @property
    def COMPRESS_NODE_MODULES(self):
        return join(self.BASE_DIR, 'components/node_modules')

    COMPRESS_PRECOMPILERS = (
        ('text/es6', 'compressor_toolkit.precompilers.ES6Compiler'),
        ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    )

    COMPRESS_ES6_COMPILER_CMD = 'export NODE_PATH="{paths}" && {browserify_bin} "{infile}" -o "{outfile}" --no-bundle-external --node -t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-es2015" ]'
