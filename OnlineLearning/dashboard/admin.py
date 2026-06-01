from django.contrib import admin

from .models import CourseAnalytics, UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'course', 'device_type', 'occurred_at']
    list_filter = ['activity_type', 'device_type']
    search_fields = ['user__email', 'course__title', 'session_key']
    date_hierarchy = 'occurred_at'


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['course', 'total_views', 'unique_viewers', 'total_watch_hours', 'active_sessions', 'engagement_score', 'last_viewed_at']
    search_fields = ['course__title']
