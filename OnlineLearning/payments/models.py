from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel, UUIDModel
from core.validators import validate_positive_decimal
from courses.models import Course

from .choices import CouponType, PaymentGateway, PaymentStatus, TransactionType


class Coupon(UUIDModel, TimeStampedModel):
    code = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=255, blank=True)
    coupon_type = models.CharField(max_length=20, choices=CouponType.choices, default=CouponType.PERCENTAGE)
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_decimal])
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_limit = models.PositiveIntegerField(default=0)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(default=timezone.now, db_index=True)
    valid_until = models.DateTimeField(null=True, blank=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    applicable_courses = models.ManyToManyField(Course, blank=True, related_name='coupons')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]

    def is_valid(self, amount=None):
        now = timezone.now()
        if not self.is_active or now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return amount is None or amount >= self.min_purchase_amount

    def calculate_discount(self, amount):
        if not self.is_valid(amount):
            return Decimal('0.00')
        if self.coupon_type == CouponType.PERCENTAGE:
            discount = amount * (self.value / Decimal('100'))
        else:
            discount = self.value
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        return min(discount, amount)

    def __str__(self):
        return self.code


class Payment(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payments')
    courses = models.ManyToManyField(Course, related_name='payments')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    gateway = models.CharField(max_length=20, choices=PaymentGateway.choices, default=PaymentGateway.RAZORPAY, db_index=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, db_index=True)
    currency = models.CharField(max_length=3, default='INR')
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_decimal])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[validate_positive_decimal])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[validate_positive_decimal])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_decimal])
    razorpay_order_id = models.CharField(max_length=120, blank=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True, db_index=True)
    stripe_payment_intent_id = models.CharField(max_length=120, blank=True, db_index=True)
    gateway_signature = models.CharField(max_length=255, blank=True)
    invoice_number = models.CharField(max_length=80, unique=True, blank=True, null=True)
    invoice_url = models.URLField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True, db_index=True)
    failure_reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['gateway', 'status']),
            models.Index(fields=['paid_at']),
            models.Index(fields=['invoice_number']),
        ]

    @property
    def is_successful(self):
        return self.status == PaymentStatus.SUCCESS

    def mark_success(self, gateway_payment_id=''):
        self.status = PaymentStatus.SUCCESS
        self.paid_at = timezone.now()
        if self.gateway == PaymentGateway.RAZORPAY:
            self.razorpay_payment_id = gateway_payment_id or self.razorpay_payment_id
        if self.gateway == PaymentGateway.STRIPE:
            self.stripe_payment_intent_id = gateway_payment_id or self.stripe_payment_intent_id
        self.save(update_fields=['status', 'paid_at', 'razorpay_payment_id', 'stripe_payment_intent_id', 'updated_at'])

    def __str__(self):
        return f'{self.user} - {self.total_amount} {self.currency}'


class Transaction(UUIDModel, TimeStampedModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, default=TransactionType.PAYMENT)
    gateway_transaction_id = models.CharField(max_length=140, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_decimal])
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, db_index=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment', 'status']),
            models.Index(fields=['gateway_transaction_id']),
            models.Index(fields=['processed_at']),
        ]

    def __str__(self):
        return self.gateway_transaction_id
