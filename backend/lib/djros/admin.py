# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

import nested_admin
from .models import CapsMan, Cap, RemoteCap, CapCoords
from .forms import CapForm, CapCoordsForm

from django.forms import TextInput, Textarea, BooleanField
from django.db import models


class CapCoordsInline(nested_admin.NestedGenericTabularInline):
    model = CapCoords
    form = CapCoordsForm
    extra = 0
    max_num = 1
    fields = ('cap', 'name', 'coords',)
    # fieldsets = (
    #     (_('Cap or RemoteCap'), {
    #         'classes': ('grp-collapse grp-open',),
    #         # 'fields': ('cap', 'name', 'coords')
    #         'fields': ('content_type', 'object_id', 'name', 'coords', 'limit')
    #     }),
    # )


class CapInline(nested_admin.NestedTabularInline):
    model = Cap
    form = CapForm
    inlines = (CapCoordsInline,)
    fields = ('name', 'radio_mac', 'bound', 'running', 'inactive', 'disabled',)
    readonly_fields = fields
    extra = 0


@admin.register(CapsMan)
class CapsManAdmin(nested_admin.NestedModelAdmin):
    list_filter = ('name', 'org')
    search_fields = ('name', 'org', 'ip_addr')
    list_display = ('name', 'org', 'ip_addr', 'num_caps', 'num_caps_disabled', 'is_active')
    fieldsets = (
        (None, {
            'fields': (
                'is_active', 'name', 'ip_addr', 'org'
            )
        }),
        (_('CAPsMAN Stats'), {
            'fields': ('num_caps', 'num_caps_disabled',)
        }),
    )
    readonly_fields = ('num_caps', 'num_caps_disabled')
    inlines = (CapInline,)

    def num_caps(self, obj):
        return obj.caps.count()
    num_caps.short_description = "Caps #"

    def num_caps_disabled(self, obj):
        return obj.caps.filter(disabled=True).count()
    num_caps_disabled.short_description = "Disabled Caps #"


class CapCoordsInline(GenericStackedInline):
    model = CapCoords
    extra = 1
    max_num = 1
    inline_classes = ('grp-collapse grp-open',)



@admin.register(Cap)
class CapAdmin(admin.ModelAdmin):
    list_display = ('name', 'radio_mac', 'bound', 'running', 'inactive', 'disabled', 'current_channel', 'num_radios')
    readonly_fields = [f.name for f in Cap._meta.fields]
    inlines = (CapCoordsInline,)
    fieldsets = (
        (_('Info'), {
            'classes': ('grp-collapse grp-open',),
            'fields': (('name', 'radio_mac', 'current_channel'),)
        }),
        (_('Status'), {
            'classes': ('grp-collapse grp-open',),
            'fields': (('bound', 'running', 'inactive', 'disabled',),)
        }),
    )
    formfield_overrides = {
        # models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},

    }
    def num_radios(self, obj):
        return obj.radios.count()
    num_radios.short_description = "Radios #"