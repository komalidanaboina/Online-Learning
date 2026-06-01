from django.contrib import admin

from .models import Cart, CartItem, CourseProgress, Enrollment, LessonProgress, Wishlist


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'enrolled_at', 'completed_at', 'expires_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['user__email', 'course__title']
    date_hierarchy = 'enrolled_at'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'created_at']
    search_fields = ['user__email', 'course__title']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'coupon_code', 'updated_at']
    list_filter = ['status']
    search_fields = ['user__email', 'coupon_code']
    inlines = [CartItemInline]


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'progress_percentage', 'completed_lessons_count', 'total_lessons_count', 'is_completed']
    list_filter = ['is_completed']
    search_fields = ['enrollment__user__email', 'enrollment__course__title']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['course_progress', 'lesson', 'is_completed', 'watch_seconds', 'completed_at']
    list_filter = ['is_completed']
    search_fields = ['lesson__title', 'course_progress__enrollment__user__email']
