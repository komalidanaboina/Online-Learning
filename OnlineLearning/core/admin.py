from django.contrib import admin

from .models import Banner, ContactMessage, FAQ, NewsletterSubscriber, SiteSettings, Testimonial


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'status', 'sort_order', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject', 'message']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_confirmed', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_confirmed']
    search_fields = ['email']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'placement', 'status', 'sort_order', 'is_active']
    list_filter = ['placement', 'status', 'is_active']
    search_fields = ['title', 'subtitle']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'status', 'is_featured']
    list_filter = ['rating', 'status', 'is_featured']
    search_fields = ['name', 'role', 'quote']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'support_email', 'maintenance_mode', 'updated_at']
