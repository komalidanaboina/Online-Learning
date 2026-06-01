from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Course, Lesson


@receiver([post_save, post_delete], sender=Lesson)
def sync_course_lesson_count(sender, instance, **kwargs):
    course = instance.section.course
    lessons_count = Lesson.objects.filter(section__course=course, is_active=True).count()
    duration = Lesson.objects.filter(section__course=course, is_active=True).values_list('duration_seconds', flat=True)
    Course.objects.filter(pk=course.pk).update(
        lessons_count=lessons_count,
        duration_minutes=sum(duration) // 60,
    )
