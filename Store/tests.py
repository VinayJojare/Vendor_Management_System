from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, Purchase, Performance


class TestPurchaseViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Contact", address="Address",
                                            vendor_code="123", on_time_delivery_rate=90.0,
                                            quality_rating_avg=4.5, average_response_time=10.0, fulfillment_rate=95.0)
        self.purchase = Purchase.objects.create(po_number="123456", vendor=self.vendor,
                                                order_date="2024-05-02T16:40:00Z",
                                                delivery_date="2024-05-03T16:41:00Z",
                                                items=[{"cloth": "Shirt"}], quantity=4, status="completed",
                                                quality_rating=3.0, issue_date="2024-05-20T16:43:00Z",
                                                acknowledgement_date="2024-05-30T16:43:00Z",
                                                quality_rating_avg=0.0)
        self.performance = Performance.objects.create(vendor=self.vendor, date="2024-05-02T20:54:00Z",
                                                      on_time_delivery_rate=53.0, quality_rating_avg=75.0,
                                                      average_response_time=5.0, fulfillment_rate=85.0)

    def test_purchase_acknowledge(self):
        url = reverse('purchase-detail', args=[self.purchase.pk])
        response = self.client.post(url + 'acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase.refresh_from_db()
        self.assertIsNotNone(self.purchase.acknowledgement_date)

    def test_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_average', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)


class TestVendorViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_vendor_list(self):
        url = reverse('vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
