from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    CustomUserAdminCreationForm,
)
from .models import CustomUser, UserProfile


class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [UserProfileInLine]

    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
