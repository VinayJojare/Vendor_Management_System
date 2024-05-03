# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VenderViewSet, PurchaseViewSet, PerformanceViewSet


router = DefaultRouter()
router.register(r'vendors', VenderViewSet)
router.register(r'purchase_orders', PurchaseViewSet)
router.register(r'performance', PerformanceViewSet)

urlpatterns = router.urls
