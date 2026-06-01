from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['student', 'instructor', 'course', 'status', 'last_message_at']
    list_filter = ['status']
    search_fields = ['student__email', 'instructor__email', 'course__title']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'message_type', 'is_seen', 'created_at']
    list_filter = ['message_type', 'is_seen']
    search_fields = ['body', 'sender__email']
