import secrets
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel, UUIDModel
from courses.models import Course
from enrollments.models import Enrollment


def certificate_upload_path(instance, filename):
    return f'certificates/{instance.user_id}/{uuid.uuid4()}-{filename}'


class Certificate(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='certificates')
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_id = models.CharField(max_length=40, unique=True, db_index=True)
    verification_code = models.CharField(max_length=64, unique=True, db_index=True)
    certificate_file = models.FileField(upload_to=certificate_upload_path, blank=True)
    issued_at = models.DateTimeField(default=timezone.now, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_revoked = models.BooleanField(default=False, db_index=True)
    revoked_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_at']
        indexes = [
            models.Index(fields=['user', '-issued_at']),
            models.Index(fields=['course', '-issued_at']),
            models.Index(fields=['verification_code', 'is_revoked']),
        ]

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = f'LH-{timezone.now():%Y%m%d}-{secrets.token_hex(5).upper()}'
        if not self.verification_code:
            self.verification_code = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    @property
    def verification_url(self):
        return f'/certificates/verify/{self.verification_code}/'

    def __str__(self):
        return self.certificate_id
