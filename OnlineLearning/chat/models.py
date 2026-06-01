import uuid

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, UUIDModel
from core.validators import document_file_validator, image_file_validator
from courses.models import Course

from .choices import ConversationStatus, MessageType


def chat_attachment_upload_path(instance, filename):
    return f'chat/{instance.conversation_id}/{uuid.uuid4()}-{filename}'


class Conversation(UUIDModel, TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_conversations')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_conversations')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    status = models.CharField(max_length=20, choices=ConversationStatus.choices, default=ConversationStatus.ACTIVE, db_index=True)
    last_message_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-last_message_at', '-updated_at']
        constraints = [models.UniqueConstraint(fields=['student', 'instructor', 'course'], name='unique_course_conversation')]
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['instructor', 'status']),
            models.Index(fields=['last_message_at']),
        ]

    def __str__(self):
        return f'{self.student} to {self.instructor}'


class Message(UUIDModel, TimeStampedModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=20, choices=MessageType.choices, default=MessageType.TEXT, db_index=True)
    body = models.TextField(blank=True)
    attachment = models.FileField(upload_to=chat_attachment_upload_path, validators=[document_file_validator], blank=True)
    image = models.ImageField(upload_to=chat_attachment_upload_path, validators=[image_file_validator], blank=True)
    is_seen = models.BooleanField(default=False, db_index=True)
    seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', '-created_at']),
            models.Index(fields=['is_seen']),
        ]

    def __str__(self):
        return f'Message from {self.sender}'
