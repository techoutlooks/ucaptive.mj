from os.path import join


class DataImportersettingsMixin(object):
    """ Basic Django configuration for our file-to-model mapper (data-importer)."""

    @property
    def IMPORTER_TEMPLATE_FILE(self):
        return join(self.MEDIA_ROOT, 'samples', 'ureporters.xls')
