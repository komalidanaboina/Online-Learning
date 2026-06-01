from django.db import models


class PublishStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class BannerPlacement(models.TextChoices):
    HOME = 'home', 'Home'
    COURSES = 'courses', 'Courses'
    DASHBOARD = 'dashboard', 'Dashboard'


class MessageStatus(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In progress'
    RESOLVED = 'resolved', 'Resolved'
    SPAM = 'spam', 'Spam'
