from django.db import models


class EnrollmentStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    EXPIRED = 'expired', 'Expired'


class CartStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CHECKED_OUT = 'checked_out', 'Checked out'
    ABANDONED = 'abandoned', 'Abandoned'
