# -*- coding: utf-8 -*-
__author__ = 'ceduth'


def run_clean(sender, instance, **kwargs):
    instance.clean()