from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError


# DATA VALIDATORS

def validate_positive_percentage(value):
    if not 0 <= value <= 100:
        raise ValidationError(
            'Value must be a positive percentage between 0 and 100 (inclusive).')


def validate_quality_rating_avg(value):
    if not 0 <= value <= 10:
        raise ValidationError(
            'Value must be a positive value between 0 and 10 (inclusive).')


def validate_positive_time_in_minutes(value):
    if value < 0:
        raise ValidationError('Value must be a non-negative time in minutes.')

# Vendor Model :


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=150)
    on_time_delivery_rate = models.FloatField(
        validators=[validate_positive_percentage])
    quality_rating_avg = models.FloatField(
        validators=[validate_quality_rating_avg])
    average_response_time = models.FloatField(
        validators=[validate_positive_time_in_minutes])
    fulfillment_rate = models.FloatField(
        validators=[validate_positive_percentage])

    class Meta:
        db_table = 'Vendor_details'


class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(unique=True, max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(
        null=True, validators=[validate_quality_rating_avg])
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'Purchase_details'


class Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(
        validators=[validate_positive_percentage])
    quality_rating_avg = models.FloatField(
        validators=[validate_quality_rating_avg])
    average_response_time = models.FloatField(
        validators=[validate_positive_time_in_minutes])
    fulfillment_rate = models.FloatField(
        validators=[validate_positive_percentage])

    class Meta:
        db_table = 'Performance_details'
