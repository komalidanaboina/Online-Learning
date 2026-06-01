from django.db import models


class CourseLevel(models.TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    ADVANCED = 'advanced', 'Advanced'
    ALL_LEVELS = 'all_levels', 'All levels'


class CourseStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    REVIEW = 'review', 'In review'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class LessonType(models.TextChoices):
    VIDEO = 'video', 'Video'
    ARTICLE = 'article', 'Article'
    LIVE = 'live', 'Live session'
    QUIZ = 'quiz', 'Quiz'
    ASSIGNMENT = 'assignment', 'Assignment'


class ResourceType(models.TextChoices):
    PDF = 'pdf', 'PDF'
    DOCUMENT = 'document', 'Document'
    VIDEO = 'video', 'Video'
    LINK = 'link', 'External link'
    ZIP = 'zip', 'Archive'


class QuestionType(models.TextChoices):
    SINGLE = 'single', 'Single choice'
    MULTIPLE = 'multiple', 'Multiple choice'
    TRUE_FALSE = 'true_false', 'True or false'
    TEXT = 'text', 'Text answer'
