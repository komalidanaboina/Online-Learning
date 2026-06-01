from django.contrib import admin

from .models import ReplyReview, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'rating', 'status', 'is_featured', 'created_at']
    list_filter = ['rating', 'status', 'is_featured']
    search_fields = ['course__title', 'user__email', 'comment', 'title']


@admin.register(ReplyReview)
class ReplyReviewAdmin(admin.ModelAdmin):
    list_display = ['review', 'instructor', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['review__course__title', 'instructor__email', 'reply']
