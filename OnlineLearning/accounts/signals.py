from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification

from .choices import UserRole
from .models import User


@receiver(post_save, sender=User)
def welcome_new_user(sender, instance, created, **kwargs):
    if not created:
        return
    title = 'Welcome to LearnHub'
    message = 'Your learning account is ready.'
    if instance.role == UserRole.INSTRUCTOR:
        message = 'Your instructor account is ready for verification.'
    Notification.objects.create(user=instance, title=title, message=message, notification_type='system')
