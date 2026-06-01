from django.db import models


class Student(models.Model):
    # Simple API demo model used to prove the DRF stack and CRUD routing work end to end.
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            # These indexes keep common API filters/searches fast as the table grows.
            models.Index(fields=['email']),
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return f'{self.name} - {self.course}'
