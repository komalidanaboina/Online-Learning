from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'user', 'course', 'issued_at', 'is_revoked']
    list_filter = ['is_revoked', 'issued_at']
    search_fields = ['certificate_id', 'verification_code', 'user__email', 'course__title']
    readonly_fields = ['certificate_id', 'verification_code', 'issued_at']
