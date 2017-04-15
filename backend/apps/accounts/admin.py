from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .models import Profile


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ('mobile_number', 'email', 'first_name', 'last_name', 'permalink',
                    'is_active', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show",
                      kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True


admin.site.register(User, UserAdmin)
