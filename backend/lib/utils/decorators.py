# -*- coding: utf-8 -*-
"""
Useful decorators.

"""


class class_property(property):
    def __get__(self, instance, type):
        if instance is None:
            return super(class_property, self).__get__(type, type)
        return super(class_property, self).__get__(instance, type)