from django.db.models.signals import post_save
from django.dispatch import receiver

from enrollments.choices import EnrollmentStatus
from enrollments.models import Enrollment

from .models import Certificate


@receiver(post_save, sender=Enrollment)
def issue_certificate_on_completion(sender, instance, **kwargs):
    if instance.status == EnrollmentStatus.COMPLETED:
        Certificate.objects.get_or_create(user=instance.user, course=instance.course, enrollment=instance)
