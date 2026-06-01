from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from courses.models import Course

from .choices import ModerationStatus
from .models import Review


def sync_course_rating(course_id):
    data = Review.objects.filter(course_id=course_id, status=ModerationStatus.APPROVED).aggregate(
        average=Avg('rating'),
        count=Count('id'),
    )
    Course.objects.filter(pk=course_id).update(
        average_rating=data['average'] or 0,
        ratings_count=data['count'] or 0,
    )


@receiver([post_save, post_delete], sender=Review)
def update_course_rating(sender, instance, **kwargs):
    sync_course_rating(instance.course_id)
