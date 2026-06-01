from django.contrib import admin

from .models import Coupon, Payment, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'value', 'used_count', 'usage_limit', 'is_active', 'valid_until']
    list_filter = ['coupon_type', 'is_active']
    search_fields = ['code', 'description']
    filter_horizontal = ['applicable_courses']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'gateway', 'status', 'total_amount', 'currency', 'paid_at', 'invoice_number']
    list_filter = ['gateway', 'status', 'currency']
    search_fields = ['user__email', 'razorpay_payment_id', 'stripe_payment_intent_id', 'invoice_number']
    filter_horizontal = ['courses']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [TransactionInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['gateway_transaction_id', 'payment', 'transaction_type', 'status', 'amount', 'processed_at']
    list_filter = ['transaction_type', 'status']
    search_fields = ['gateway_transaction_id', 'payment__user__email']
