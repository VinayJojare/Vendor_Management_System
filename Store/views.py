from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Vendor, Purchase, Performance
from .serializers import Venderserializer, Purchaseserialiazer, Performanceserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from rest_framework import status


class VenderViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = Venderserializer


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = Purchaseserialiazer

    def acknowledge(self, request, pk=None):
        purchase = self.get_object()
        purchase.acknowledgment_date = timezone.now()
        purchase.save()

        # Trigger recalculation of average_response_time
        vendor = purchase.vendor
        # Create an instance of VendorPerformanceAPIView
        vendor_performance_view = VendorPerformanceAPIView()
        average_response_time = vendor_performance_view.calculate_average_response_time(
            vendor)

        return Response(
            {"acknowledgment_date": purchase.acknowledgment_date,
                "average_response_time": average_response_time},
            status=status.HTTP_200_OK,
        )


class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = Performanceserializer


class VendorPerformanceAPIView(APIView):

    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)

        on_time_delivery_rate = self.calculate_on_time_delivery_rate(vendor)
        quality_rating_average = self.calculate_quality_rating_average(vendor)
        average_response_time = self.calculate_average_response_time(vendor)
        fulfillment_rate = self.calculate_fulfillment_rate(vendor)

        return Response(
            {
                "on_time_delivery_rate": on_time_delivery_rate,
                "quality_rating_average": quality_rating_average,
                "average_response_time": average_response_time,
                "fulfillment_rate": fulfillment_rate,
            },
            status=status.HTTP_200_OK,
        )

    # on_time_delivery_rate
    def calculate_on_time_delivery_rate(self, vendor):
        completed_pos = Purchase.objects.filter(
            vendor=vendor, status="completed")
        completed_on_time = completed_pos.filter(
            delivery_date__lte=timezone.now())
        on_time = completed_on_time.count()
        total_completed = completed_pos.count()
        return (on_time / total_completed) * 100 if total_completed > 0 else 0

    # quality_rating_average
    def calculate_quality_rating_average(self, vendor):
        completed_pos_with_rating = Purchase.objects.filter(
            vendor=vendor, status="completed", quality_rating__isnull=False
        )
        quality_rating_average = completed_pos_with_rating.aggregate(
            Avg("quality_rating")
        )["quality_rating__avg"]
        return quality_rating_average if quality_rating_average is not None else 0

    # average_response_time
    def calculate_average_response_time(self, vendor):
        acknowledged_pos = Purchase.objects.filter(
            vendor=vendor, order_date__isnull=False
        )
        response_times = [
            (po.order_date - po.issue_date).total_seconds() / 3600
            for po in acknowledged_pos
        ]
        average_response_time = (
            sum(response_times) / len(response_times)
        ) if response_times else None
        return round(average_response_time, 2) if average_response_time is not None else None

    # fulfillment_rate

    def calculate_fulfillment_rate(self, vendor):
        total_pos = Purchase.objects.filter(vendor=vendor).count()
        if total_pos == 0:
            return 0
        fulfilled_pos = Purchase.objects.filter(
            vendor=vendor, status="completed"
        ).count()
        return (fulfilled_pos / total_pos) * 100
