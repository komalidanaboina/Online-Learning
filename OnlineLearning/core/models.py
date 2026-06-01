import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from .choices import BannerPlacement, MessageStatus, PublishStatus
from .managers import ActiveManager, AllObjectsManager
from .validators import image_file_validator


def banner_upload_path(instance, filename):
    return f'banners/{instance.placement}/{uuid.uuid4()}-{filename}'


def testimonial_upload_path(instance, filename):
    return f'testimonials/{uuid.uuid4()}-{filename}'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])


class FAQ(UUIDModel, TimeStampedModel, SoftDeleteModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    status = models.CharField(max_length=20, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED, db_index=True)

    class Meta:
        ordering = ['sort_order', 'question']
        indexes = [
            models.Index(fields=['status', 'sort_order']),
            models.Index(fields=['is_active', 'deleted_at']),
        ]

    def __str__(self):
        return self.question


class ContactMessage(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=MessageStatus.choices, default=MessageStatus.NEW, db_index=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email', '-created_at']),
        ]

    def __str__(self):
        return f'{self.subject} - {self.email}'


class NewsletterSubscriber(UUIDModel, TimeStampedModel):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False, db_index=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['is_confirmed', '-created_at'])]

    @property
    def is_subscribed(self):
        return self.unsubscribed_at is None

    def __str__(self):
        return self.email


class Banner(UUIDModel, TimeStampedModel, SoftDeleteModel):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=banner_upload_path, validators=[image_file_validator])
    placement = models.CharField(max_length=30, choices=BannerPlacement.choices, default=BannerPlacement.HOME, db_index=True)
    cta_text = models.CharField(max_length=80, blank=True)
    cta_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT, db_index=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['placement', 'status', 'sort_order']),
            models.Index(fields=['starts_at', 'ends_at']),
        ]

    def __str__(self):
        return self.title


class Testimonial(UUIDModel, TimeStampedModel, SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to=testimonial_upload_path, validators=[image_file_validator], blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    status = models.CharField(max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f'{self.name} testimonial'


class SiteSettings(UUIDModel, TimeStampedModel):
    site_name = models.CharField(max_length=120, default='LearnHub')
    support_email = models.EmailField()
    support_phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', validators=[image_file_validator], blank=True)
    favicon = models.ImageField(upload_to='site/', validators=[image_file_validator], blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    maintenance_mode = models.BooleanField(default=False)
    terms_url = models.URLField(blank=True)
    privacy_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'site settings'
        verbose_name_plural = 'site settings'

    def __str__(self):
        return self.site_name
