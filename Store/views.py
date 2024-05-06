from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Vendor, Purchase, Performance
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class VenderViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = Venderserializer


class PurchaseViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()
    serializer_class = Purchaseserialiazer

    def acknowledge(self, request, pk=None):
        purchase = self.get_object()
        purchase.acknowledgment_date = timezone.now()
        purchase.save()
        vendor = purchase.vendor
        vendor_performance_view = VendorPerformanceAPIView()
        average_response_time = vendor_performance_view.calculate_average_response_time(
            vendor)
        return Response(
            {"acknowledgment_date": purchase.acknowledgment_date,
                "average_response_time": average_response_time},
            status=status.HTTP_200_OK,
        )


class PerformanceViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Performance.objects.all()
    serializer_class = Performanceserializer


class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        on_time_delivery_rate = self.calculate_on_time_delivery_rate(vendor)
        quality_rating_average = self.calculate_quality_rating_average(vendor)
        average_response_time = self.calculate_average_response_time(vendor)
        fulfillment_rate = self.calculate_fulfillment_rate(vendor)
        on_time_delivery_rate_percent = "{:.2f}%".format(on_time_delivery_rate)
        fulfillment_rate_percent = "{:.2f}%".format(fulfillment_rate)
        quality_rating_out_of_10 = "{:.2f}".format(
            quality_rating_average / 10) if quality_rating_average is not None else None
        average_response_time_min = "{:.2f} min".format(
            average_response_time) if average_response_time is not None else None
        return Response(
            {
                "on_time_delivery_rate": on_time_delivery_rate_percent,
                "quality_rating_average": quality_rating_out_of_10,
                "average_response_time": average_response_time_min,
                "fulfillment_rate": fulfillment_rate_percent,
            },
            status=status.HTTP_200_OK,
        )

    def calculate_on_time_delivery_rate(self, vendor):
        completed_pos = Purchase.objects.filter(
            vendor=vendor, status="completed"
        )
        completed_on_time = completed_pos.filter(
            delivery_date__lte=timezone.now()
        )
        on_time = completed_on_time.count()
        total_completed = completed_pos.count()
        return (on_time / total_completed) * 100 if total_completed > 0 else 0

    def calculate_quality_rating_average(self, vendor):
        completed_pos_with_rating = Purchase.objects.filter(
            vendor=vendor, status="completed", quality_rating__isnull=False
        )
        quality_rating_average = completed_pos_with_rating.aggregate(
            Avg("quality_rating")
        )["quality_rating__avg"]
        return quality_rating_average if quality_rating_average is not None else 0

    def calculate_average_response_time(self, vendor):
        acknowledged_pos = Purchase.objects.filter(
            vendor=vendor, order_date__isnull=False
        )
        response_times = [
            (po.order_date - po.issue_date).total_seconds() / 60
            for po in acknowledged_pos
        ]
        average_response_time = (
            sum(response_times) / len(response_times)
        ) if response_times else None
        return average_response_time

    def calculate_fulfillment_rate(self, vendor):
        total_pos = Purchase.objects.filter(vendor=vendor).count()
        if total_pos == 0:
            return 0
        fulfilled_pos = Purchase.objects.filter(
            vendor=vendor, status="completed"
        ).count()
        return (fulfilled_pos / total_pos) * 100


class RegisterUserViewSet(APIView):
    def post(self, request):
        serializer = UserSerialazer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': "not valid user!"})
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj), 'message': 'Success'})
