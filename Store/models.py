from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta

# Vendor Model :


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=150)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        db_table = 'Vendor_details'


# Purchase Model
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
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)
    quality_rating_avg = models.FloatField(default=0.0)

    class Meta:
        db_table = 'Purchase_details'


# Performance Model:

class Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        db_table = 'Performance_details'
