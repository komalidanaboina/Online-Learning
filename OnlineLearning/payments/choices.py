from django.db import models


class PaymentGateway(models.TextChoices):
    RAZORPAY = 'razorpay', 'Razorpay'
    STRIPE = 'stripe', 'Stripe'
    MANUAL = 'manual', 'Manual'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'
    CANCELLED = 'cancelled', 'Cancelled'


class CouponType(models.TextChoices):
    PERCENTAGE = 'percentage', 'Percentage'
    FIXED = 'fixed', 'Fixed amount'


class TransactionType(models.TextChoices):
    PAYMENT = 'payment', 'Payment'
    REFUND = 'refund', 'Refund'
    ADJUSTMENT = 'adjustment', 'Adjustment'
