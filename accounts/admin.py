from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, KioskOperatorProfile, SuperAgentProfile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "user_type", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


class KioskOperatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "kiosk_location", "latitude", "longitude")
    readonly_fields = ("latitude", "longitude")


admin.site.register(User, CustomUserAdmin)
admin.site.register(KioskOperatorProfile, KioskOperatorProfileAdmin)
admin.site.register(SuperAgentProfile)
