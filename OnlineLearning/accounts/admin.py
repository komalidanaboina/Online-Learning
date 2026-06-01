from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['-created_at']
    list_display = ['email', 'full_name', 'role', 'verification_status', 'is_active', 'is_email_verified', 'last_seen']
    list_filter = ['role', 'verification_status', 'is_active', 'is_staff', 'is_email_verified']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number', 'city', 'country']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image', 'bio', 'phone_number', 'gender', 'date_of_birth')}),
        ('Role and verification', {'fields': ('role', 'verification_status', 'verification_notes', 'is_email_verified', 'is_phone_verified')}),
        ('Location and profile', {'fields': ('country', 'state', 'city', 'timezone', 'social_links', 'education', 'skills', 'experience')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_seen', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
