# -*- coding: utf-8 -*-
"""
Utils for django model classes.

"""
from django.db import models
from django.db.models import Q


class ModelFactoryMixin(object):

    @classmethod
    def parse_model_data(cls, model=None, exclude=[], **kwargs):
        """
        Return only the subset of kwargs that belongs to 'model',
        """
        m = model or cls
        for prop in kwargs.keys():
            if prop not in [f.name for f in m._meta.fields] or prop in exclude:
                kwargs.pop(prop)
        return kwargs

    @classmethod
    def update_or_create(cls, defaults=None, **kwargs):
        """
        A convenience method for updating an object with the given kwargs, creating a new one if necessary.
        Returns the created instance.

        Applies to this model if no model given.
        """
        try:
            obj = cls.objects.get(**kwargs)
            if defaults:
                for k, v in defaults.items():
                    setattr(obj, k, v)
                obj.save()
        except cls.DoesNotExist:
            kwargs.update(defaults)
            obj = cls(**kwargs)
            obj.save()
        return obj


class FKeyModelFactoryMixin(ModelFactoryMixin):
    """

    """

    @staticmethod
    def get_fk_model(model, fieldname):
        """
        returns None if not foreignkey, otherwise the relevant model
        """

        field_object, model, direct, m2m = model._meta.get_field_by_name(fieldname)
        if not m2m and direct and isinstance(field_object, models.ForeignKey):
            return field_object.rel.to
        return None

    @classmethod
    def get_fk_models(cls, model=None):
        """
        Get all foreign models
        """
        m = model or cls
        return filter(None, [cls.get_fk_model(m._meta.model, f) for f in [f.name for f in m._meta.fields]])

    @classmethod
    def get_related_fk_fields(cls):
        pass

    @classmethod
    def get_fk_instance(cls, fk_name, model=None, match='icontains', **kwargs):
        """
        Given a fk field name in 'model', return fk instance that matches the criteria,
        if found, or None. Applies to this model (cls) if no model given.
        """
        if kwargs:
            opts = {}
            for prop in kwargs.keys(): opts.update({"%s__{}".format(match) % prop: kwargs.get(prop)})
            print "get_fk_instance:: model=%s fk_name=%s opts=%s" % (model, fk_name, opts)
            obj = model.objects.filter(Q(**opts)).first()
            print obj
            return obj

    @classmethod
    def update_or_create_related(cls, fk_name, model=None, match='icontains', defaults=None, **kwargs):
        """
        Given a fk field name in 'model', update or create (if non existent) an instance of that
        related model using given kwargs; and update/set the instance in parent ('model').
        Returns the created instance.

        Applies to this model if no model given.
        """
        try:
            obj = cls.get_fk_instance(fk_name, model, match, **kwargs)
            if defaults:
                for k, v in defaults:
                    setattr(obj, k, v)
                obj.save()
        except cls.DoesNotExist:
            kwargs.update(defaults)
            obj = cls(**kwargs)
            obj.save()
        return obj


