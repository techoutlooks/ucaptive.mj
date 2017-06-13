

class UreportersSettingsMixins(object):

    #  django-guardian
    def AUTHENTICATION_BACKENDS(self):
        return super(UreportersSettingsMixins, self).AUTHENTICATION_BACKENDS + (
            'guardian.backends.ObjectPermissionBackend',
        )