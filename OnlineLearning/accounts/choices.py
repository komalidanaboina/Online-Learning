from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', 'Student'
    INSTRUCTOR = 'instructor', 'Instructor'
    ADMIN = 'admin', 'Admin'


class VerificationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    VERIFIED = 'verified', 'Verified'
    REJECTED = 'rejected', 'Rejected'


class Gender(models.TextChoices):
    FEMALE = 'female', 'Female'
    MALE = 'male', 'Male'
    OTHER = 'other', 'Other'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say', 'Prefer not to say'
