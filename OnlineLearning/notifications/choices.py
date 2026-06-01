from django.db import models


class NotificationType(models.TextChoices):
    SYSTEM = 'system', 'System'
    COURSE = 'course', 'Course'
    PAYMENT = 'payment', 'Payment'
    CERTIFICATE = 'certificate', 'Certificate'
    MESSAGE = 'message', 'Message'
