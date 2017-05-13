from django.contrib import admin
from .models import Org #, Employee

from rest_framework_api_key.admin import ApiKeyAdmin
from .models import OrgApiKeyToken


@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
        pass


# @admin.register(Employee)
# class OrgAdmin(admin.ModelAdmin):
#     pass


# TODO: Permissions. django-guardian??

@admin.register(OrgApiKeyToken)
class OrgApiKeyAdmin(ApiKeyAdmin):
    new_required_fields = ('org',)
    list_display = new_required_fields + ('id', 'name', 'created', 'modified')

    fieldsets = (
        ('Required Information', {'fields': ('name',) + new_required_fields}),
        ('Additional Information', {'fields': ('key_message',)}),
    )

    def save_model(self, request, obj, form, change):
        # obj.orgs = request.
        super(OrgApiKeyAdmin, self).save_model(request, obj, form, change)

