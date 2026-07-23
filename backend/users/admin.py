from django.contrib import admin
from .models import CustomUser, ActivityLog, SessionManagement


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_email_verified', 'is_active', 'created_at')
    list_filter = ('role', 'is_email_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Credentials', {'fields': ('username', 'password')}),
        ('Role & Department', {'fields': ('role', 'department', 'badge_number')}),
        ('Verification', {'fields': ('is_email_verified', 'email_verification_token')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at', 'user')
    search_fields = ('user__username', 'description')
    readonly_fields = ('action_hash', 'created_at')


@admin.register(SessionManagement)
class SessionManagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'logged_in_at', 'last_activity', 'is_active')
    list_filter = ('is_active', 'logged_in_at', 'user')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('logged_in_at', 'last_activity')
