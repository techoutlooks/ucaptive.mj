_RADIUS_APP_NAME = 'freeradius'
_RADIUS_DB_NAME = 'radius'      # same as FreeRadius v3

class RadiusRouter(object):
    """
    A router to control all database operations on models in
    the freeradius application
    
    """

    def db_for_read(self, model, **hints):
        """ 
        Point all operations on myapp models to 'other'
        
        """
        if model._meta.app_label == _RADIUS_APP_NAME:
            return _RADIUS_DB_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on myapp models to 'other'
        
        """
        if model._meta.app_label == _RADIUS_APP_NAME:
            return _RADIUS_DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if a model in myapp is involved
        
        """
        return None
        #return obj1._meta.app_label == obj2._meta.app_label

    def allow_migrate(self, db, model):
        """
        Make sure the freeradius app only appears on the 'freeradius' db
        
        """
        if db == _RADIUS_DB_NAME:
            return model._meta.app_label == _RADIUS_APP_NAME
        elif model._meta.app_label == _RADIUS_APP_NAME:
            return False
        return None
