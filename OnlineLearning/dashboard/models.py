from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel, UUIDModel
from courses.models import Course

from .choices import ActivityType, DeviceType


class UserActivity(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_activities')
    session_key = models.CharField(max_length=80, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, choices=DeviceType.choices, default=DeviceType.UNKNOWN, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['user', 'activity_type', '-occurred_at']),
            models.Index(fields=['course', 'activity_type']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f'{self.user} - {self.activity_type}'


class CourseAnalytics(UUIDModel, TimeStampedModel):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='analytics')
    total_views = models.PositiveIntegerField(default=0, db_index=True)
    unique_viewers = models.PositiveIntegerField(default=0)
    total_watch_seconds = models.PositiveBigIntegerField(default=0)
    average_watch_seconds = models.PositiveIntegerField(default=0)
    active_sessions = models.PositiveIntegerField(default=0, db_index=True)
    engagement_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_index=True)
    last_viewed_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-engagement_score']
        verbose_name_plural = 'course analytics'
        indexes = [
            models.Index(fields=['total_views']),
            models.Index(fields=['engagement_score']),
            models.Index(fields=['last_viewed_at']),
        ]

    @property
    def total_watch_hours(self):
        return round(self.total_watch_seconds / 3600, 2)

    def __str__(self):
        return f'{self.course} analytics'
