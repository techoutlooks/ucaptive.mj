from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .models import Profile
from .forms import NgProfileForm, UserAdminChangeForm


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile
    # form = NgProfileForm
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'reporter'


class UserAdmin(GuardedModelAdmin):
    form = UserAdminChangeForm
    search_fields = ('mobile_number', 'first_name', 'last_name')
    inlines = [UserProfileInline]
    list_display = ('mobile_number', 'email', 'first_name', 'last_name',# 'permalink',
                    'is_active', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        if obj.profile:
            url = reverse("profiles:show",
                          kwargs={"slug": obj.profile.slug})
            # Unicode hex b6 is the Pilcrow sign
            return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = _("Full Name")

admin.site.register(User, UserAdmin)
admin.site.register(Group)