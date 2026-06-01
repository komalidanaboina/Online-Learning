from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .choices import ActivityType
from .models import CourseAnalytics, UserActivity


@receiver(post_save, sender=UserActivity)
def update_course_analytics(sender, instance, created, **kwargs):
    if not created or not instance.course_id:
        return
    analytics, _ = CourseAnalytics.objects.get_or_create(course=instance.course)
    if instance.activity_type == ActivityType.COURSE_VIEW:
        CourseAnalytics.objects.filter(pk=analytics.pk).update(
            total_views=F('total_views') + 1,
            last_viewed_at=timezone.now(),
        )
    elif instance.activity_type == ActivityType.LESSON_WATCH:
        seconds = int(instance.metadata.get('watch_seconds', 0) or 0)
        CourseAnalytics.objects.filter(pk=analytics.pk).update(
            total_watch_seconds=F('total_watch_seconds') + seconds,
            last_viewed_at=timezone.now(),
        )
