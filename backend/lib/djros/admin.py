# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from django.contrib import admin
from .models import CapsMan, Cap, RemoteCap

# Register your models here.


@admin.register(CapsMan)
class CapsManAdmin(admin.ModelAdmin):
    list_filter = ('name', 'org')
    search_fields = ('name', 'org', 'ip_addr')
    list_display = ('name', 'org', 'ip_addr', 'num_caps', 'num_caps_disabled' , 'is_active')

    def num_caps(self, obj):
        return obj.caps.count()
    num_caps.short_description = "Caps #"

    def num_caps_disabled(self, obj):
        return obj.caps.filter(disabled=True).count()
    num_caps_disabled.short_description = "Disabled Caps #"


# TODO: CapInline