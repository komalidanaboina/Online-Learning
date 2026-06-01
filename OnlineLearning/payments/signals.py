from django.db.models.signals import post_save
from django.dispatch import receiver

from enrollments.models import Enrollment

from .choices import PaymentStatus
from .models import Payment


@receiver(post_save, sender=Payment)
def enroll_after_successful_payment(sender, instance, created, **kwargs):
    if instance.status != PaymentStatus.SUCCESS:
        return
    for course in instance.courses.all():
        Enrollment.objects.get_or_create(user=instance.user, course=course, defaults={'source': 'payment'})
