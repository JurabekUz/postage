from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'branch', 'first_name', 'last_name', 'email', 'is_staff']
    list_filter = ['branch']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "branch")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    # "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        )
    )


from django.contrib.auth.models import Group

# Unregister the Group model
admin.site.unregister(Group)

# Example for JWT-related models if using djangorestframework-simplejwt
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Unregister JWT-related models
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
