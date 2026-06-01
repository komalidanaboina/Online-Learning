from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from courses.models import Course

from .models import CourseProgress, Enrollment


@receiver(post_save, sender=Enrollment)
def create_course_progress(sender, instance, created, **kwargs):
    if created:
        CourseProgress.objects.get_or_create(enrollment=instance)
        Course.objects.filter(pk=instance.course_id).update(enrollments_count=F('enrollments_count') + 1)


@receiver(post_delete, sender=Enrollment)
def decrement_course_enrollment_count(sender, instance, **kwargs):
    Course.objects.filter(pk=instance.course_id, enrollments_count__gt=0).update(enrollments_count=F('enrollments_count') - 1)
