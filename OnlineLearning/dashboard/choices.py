from django.db import models


class ActivityType(models.TextChoices):
    LOGIN = 'login', 'Login'
    LOGOUT = 'logout', 'Logout'
    COURSE_VIEW = 'course_view', 'Course view'
    LESSON_WATCH = 'lesson_watch', 'Lesson watch'
    QUIZ_ATTEMPT = 'quiz_attempt', 'Quiz attempt'
    PURCHASE = 'purchase', 'Purchase'


class DeviceType(models.TextChoices):
    DESKTOP = 'desktop', 'Desktop'
    MOBILE = 'mobile', 'Mobile'
    TABLET = 'tablet', 'Tablet'
    UNKNOWN = 'unknown', 'Unknown'
