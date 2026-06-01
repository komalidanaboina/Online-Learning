import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.validators import image_file_validator

from .choices import Gender, UserRole, VerificationStatus
from .managers import InstructorManager, UserManager
from .validators import phone_validator, validate_skill_list, validate_social_links


def user_avatar_upload_path(instance, filename):
    return f'users/{instance.id}/avatar/{uuid.uuid4()}-{filename}'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT, db_index=True)
    profile_image = models.ImageField(upload_to=user_avatar_upload_path, validators=[image_file_validator], blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, validators=[phone_validator], blank=True, db_index=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True, validators=[validate_social_links])
    education = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True, validators=[validate_skill_list])
    experience = models.JSONField(default=list, blank=True)
    country = models.CharField(max_length=80, blank=True, db_index=True)
    state = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True, db_index=True)
    timezone = models.CharField(max_length=64, blank=True)
    is_email_verified = models.BooleanField(default=False, db_index=True)
    is_phone_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )
    verification_notes = models.TextField(blank=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    instructors = InstructorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role', 'verification_status']),
            models.Index(fields=['is_active', 'is_email_verified']),
            models.Index(fields=['country', 'city']),
            models.Index(fields=['last_seen']),
        ]

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def full_name(self):
        return self.get_full_name() or self.email

    @property
    def is_student(self):
        return self.role == UserRole.STUDENT

    @property
    def is_instructor(self):
        return self.role == UserRole.INSTRUCTOR

    @property
    def is_platform_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    def mark_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=['last_seen'])
