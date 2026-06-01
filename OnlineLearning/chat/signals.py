from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def update_conversation_last_message(sender, instance, created, **kwargs):
    if created:
        instance.conversation.last_message_at = instance.created_at
        instance.conversation.save(update_fields=['last_message_at', 'updated_at'])
