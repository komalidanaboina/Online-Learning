from django.contrib import admin

from .models import Assignment, Category, Choice, Course, Lesson, Question, Quiz, Resource, Section, SubCategory, Tag


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'sort_order', 'is_active']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'sort_order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'status', 'price', 'discount_price', 'average_rating', 'enrollments_count', 'is_featured']
    list_filter = ['status', 'level', 'language', 'is_featured', 'category']
    search_fields = ['title', 'short_description', 'instructor__email', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['id', 'average_rating', 'ratings_count', 'enrollments_count', 'lessons_count', 'created_at', 'updated_at']
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'sort_order', 'is_active']
    list_filter = ['course', 'is_active']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'lesson_type', 'duration_seconds', 'sort_order', 'is_preview', 'is_active']
    list_filter = ['lesson_type', 'is_preview', 'is_active']
    search_fields = ['title', 'section__course__title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'resource_type', 'is_downloadable']
    list_filter = ['resource_type', 'is_downloadable']
    search_fields = ['title', 'lesson__title']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'pass_percentage', 'time_limit_minutes', 'allow_retake']
    search_fields = ['title', 'lesson__title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'sort_order']
    list_filter = ['question_type']
    search_fields = ['question_text', 'quiz__title']
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct', 'sort_order']
    list_filter = ['is_correct']
    search_fields = ['choice_text', 'question__question_text']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'due_days', 'max_score', 'is_active']
    search_fields = ['title', 'lesson__title']
