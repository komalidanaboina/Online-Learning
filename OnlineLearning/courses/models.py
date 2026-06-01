import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.models import SoftDeleteModel, TimeStampedModel, UUIDModel
from core.validators import document_file_validator, image_file_validator, validate_positive_decimal, video_file_validator

from .choices import CourseLevel, CourseStatus, LessonType, QuestionType, ResourceType
from .managers import PublishedCourseManager
from .validators import validate_discount_price, validate_json_string_list


def course_thumbnail_upload_path(instance, filename):
    return f'courses/{instance.id}/thumbnail/{uuid.uuid4()}-{filename}'


def course_preview_upload_path(instance, filename):
    return f'courses/{instance.id}/preview/{uuid.uuid4()}-{filename}'


def lesson_video_upload_path(instance, filename):
    return f'courses/{instance.section.course_id}/lessons/{instance.id}/{uuid.uuid4()}-{filename}'


def resource_upload_path(instance, filename):
    return f'courses/{instance.lesson.section.course_id}/resources/{uuid.uuid4()}-{filename}'


class Tag(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['slug'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(UUIDModel, TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to='categories/', validators=[image_file_validator], blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured', 'sort_order']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(UUIDModel, TimeStampedModel, SoftDeleteModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['category__name', 'sort_order', 'name']
        verbose_name_plural = 'subcategories'
        constraints = [models.UniqueConstraint(fields=['category', 'slug'], name='unique_subcategory_slug_per_category')]
        indexes = [
            models.Index(fields=['category', 'slug']),
            models.Index(fields=['sort_order']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.name}'


class Course(UUIDModel, TimeStampedModel, SoftDeleteModel):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='courses_taught')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    tags = models.ManyToManyField(Tag, blank=True, related_name='courses')
    title = models.CharField(max_length=180, db_index=True)
    slug = models.SlugField(max_length=220, unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=course_thumbnail_upload_path, validators=[image_file_validator])
    preview_video = models.FileField(upload_to=course_preview_upload_path, validators=[video_file_validator], blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[validate_positive_decimal])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[validate_positive_decimal])
    currency = models.CharField(max_length=3, default='INR')
    level = models.CharField(max_length=20, choices=CourseLevel.choices, default=CourseLevel.BEGINNER, db_index=True)
    language = models.CharField(max_length=50, default='English', db_index=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    learning_outcomes = models.JSONField(default=list, validators=[validate_json_string_list], blank=True)
    requirements = models.JSONField(default=list, validators=[validate_json_string_list], blank=True)
    target_audience = models.JSONField(default=list, validators=[validate_json_string_list], blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], db_index=True)
    ratings_count = models.PositiveIntegerField(default=0)
    enrollments_count = models.PositiveIntegerField(default=0, db_index=True)
    lessons_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, db_index=True)
    status = models.CharField(max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    objects = models.Manager()
    published = PublishedCourseManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['instructor', 'status']),
            models.Index(fields=['is_featured', 'average_rating']),
            models.Index(fields=['price', 'discount_price']),
            models.Index(fields=['slug']),
        ]

    def clean(self):
        validate_discount_price(self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == CourseStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price is not None else self.price

    @property
    def discount_percentage(self):
        if not self.discount_price or not self.price:
            return 0
        return round(((self.price - self.discount_price) / self.price) * 100)

    @property
    def is_free(self):
        return self.effective_price == 0

    def __str__(self):
        return self.title


class Section(UUIDModel, TimeStampedModel, SoftDeleteModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['sort_order', 'created_at']
        constraints = [models.UniqueConstraint(fields=['course', 'sort_order'], name='unique_section_order_per_course')]
        indexes = [models.Index(fields=['course', 'sort_order'])]

    def __str__(self):
        return f'{self.course} - {self.title}'


class Lesson(UUIDModel, TimeStampedModel, SoftDeleteModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220)
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices, default=LessonType.VIDEO, db_index=True)
    content = models.TextField(blank=True)
    video = models.FileField(upload_to=lesson_video_upload_path, validators=[video_file_validator], blank=True)
    video_url = models.URLField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_preview = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['sort_order', 'created_at']
        constraints = [
            models.UniqueConstraint(fields=['section', 'slug'], name='unique_lesson_slug_per_section'),
            models.UniqueConstraint(fields=['section', 'sort_order'], name='unique_lesson_order_per_section'),
        ]
        indexes = [
            models.Index(fields=['section', 'sort_order']),
            models.Index(fields=['lesson_type', 'is_preview']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Resource(UUIDModel, TimeStampedModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=160)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices, default=ResourceType.PDF)
    file = models.FileField(upload_to=resource_upload_path, validators=[document_file_validator], blank=True)
    external_url = models.URLField(blank=True)
    is_downloadable = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=['lesson', 'resource_type'])]

    def __str__(self):
        return self.title


class Quiz(UUIDModel, TimeStampedModel, SoftDeleteModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=180)
    instructions = models.TextField(blank=True)
    pass_percentage = models.PositiveSmallIntegerField(default=70, validators=[MinValueValidator(1), MaxValueValidator(100)])
    time_limit_minutes = models.PositiveIntegerField(default=0)
    allow_retake = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Question(UUIDModel, TimeStampedModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.SINGLE)
    points = models.PositiveSmallIntegerField(default=1)
    sort_order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['sort_order']
        indexes = [models.Index(fields=['quiz', 'sort_order'])]

    def __str__(self):
        return self.question_text[:80]


class Choice(UUIDModel, TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        indexes = [models.Index(fields=['question', 'is_correct'])]

    def __str__(self):
        return self.choice_text


class Assignment(UUIDModel, TimeStampedModel, SoftDeleteModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='assignment')
    title = models.CharField(max_length=180)
    instructions = models.TextField()
    due_days = models.PositiveIntegerField(default=7)
    max_score = models.PositiveIntegerField(default=100)
    rubric = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
