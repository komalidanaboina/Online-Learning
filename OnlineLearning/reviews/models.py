from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import TimeStampedModel, UUIDModel
from courses.models import Course

from .choices import ModerationStatus


class Review(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
    title = models.CharField(max_length=160, blank=True)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=ModerationStatus.choices, default=ModerationStatus.PENDING, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='unique_review_per_user_course')]
        indexes = [
            models.Index(fields=['course', 'status', '-created_at']),
            models.Index(fields=['rating', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self):
        return f'{self.course} - {self.rating}'


class ReplyReview(UUIDModel, TimeStampedModel):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_replies')
    reply = models.TextField()
    status = models.CharField(max_length=20, choices=ModerationStatus.choices, default=ModerationStatus.APPROVED, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['instructor', 'status'])]

    def __str__(self):
        return f'Reply to {self.review_id}'
