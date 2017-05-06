# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save

from .models import Cap, RemoteCap
from .signals import run_clean


class DJROSConfig(AppConfig):
    name = 'djros'
    verbose_name = _('Django RouterOS')

    def ready(self):
        pre_save.connect(run_clean, sender=Cap)
        pre_save.connect(run_clean, sender=RemoteCap)