from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel, UUIDModel
from courses.models import Course, Lesson

from .choices import CartStatus, EnrollmentStatus


class Enrollment(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='enrollments')
    status = models.CharField(max_length=20, choices=EnrollmentStatus.choices, default=EnrollmentStatus.ACTIVE, db_index=True)
    enrolled_at = models.DateTimeField(default=timezone.now, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['-enrolled_at']
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course_enrollment')]
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['course', 'status']),
            models.Index(fields=['enrolled_at']),
        ]

    def __str__(self):
        return f'{self.user} enrolled in {self.course}'


class Wishlist(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='unique_wishlist_course_per_user')]
        indexes = [models.Index(fields=['user', '-created_at'])]

    def __str__(self):
        return f'{self.user} saved {self.course}'


class Cart(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=20, choices=CartStatus.choices, default=CartStatus.ACTIVE, db_index=True)
    coupon_code = models.CharField(max_length=40, blank=True, db_index=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [models.Index(fields=['user', 'status'])]

    @property
    def total_amount(self):
        return sum(item.course.effective_price for item in self.items.select_related('course'))

    def __str__(self):
        return f'{self.user} cart'


class CartItem(UUIDModel, TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_items')
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['cart', 'course'], name='unique_course_per_cart')]
        indexes = [models.Index(fields=['cart', 'course'])]

    def save(self, *args, **kwargs):
        if self.price_at_add is None:
            self.price_at_add = self.course.effective_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course} in cart'


class CourseProgress(UUIDModel, TimeStampedModel):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='progress')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], db_index=True)
    completed_lessons_count = models.PositiveIntegerField(default=0)
    total_lessons_count = models.PositiveIntegerField(default=0)
    last_accessed_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_accessed_by')
    is_completed = models.BooleanField(default=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_completed', 'progress_percentage']),
            models.Index(fields=['updated_at']),
        ]

    def recalculate(self):
        total = self.enrollment.course.lessons_count or Lesson.objects.filter(section__course=self.enrollment.course, is_active=True).count()
        completed = LessonProgress.objects.filter(course_progress=self, is_completed=True).count()
        self.total_lessons_count = total
        self.completed_lessons_count = completed
        self.progress_percentage = round((completed / total) * 100, 2) if total else 0
        self.is_completed = total > 0 and completed >= total
        self.completed_at = timezone.now() if self.is_completed and not self.completed_at else self.completed_at
        self.save()

    def __str__(self):
        return f'{self.enrollment} progress'


class LessonProgress(UUIDModel, TimeStampedModel):
    course_progress = models.ForeignKey(CourseProgress, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    is_completed = models.BooleanField(default=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    watch_seconds = models.PositiveIntegerField(default=0)
    last_position_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-updated_at']
        constraints = [models.UniqueConstraint(fields=['course_progress', 'lesson'], name='unique_lesson_progress')]
        indexes = [
            models.Index(fields=['course_progress', 'is_completed']),
            models.Index(fields=['lesson', 'is_completed']),
        ]

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=['is_completed', 'completed_at', 'updated_at'])
        self.course_progress.recalculate()

    def __str__(self):
        return f'{self.lesson} progress'
