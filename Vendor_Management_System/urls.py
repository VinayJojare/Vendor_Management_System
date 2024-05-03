"""
URL configuration for Vendor_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Store.views import VendorPerformanceAPIView, PurchaseViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Store.urls')),
    path('', include('rest_framework.urls')),
    path('api/vendors/<int:vendor_id>/performance/',
         VendorPerformanceAPIView.as_view()),
    path("api/purchase_orders/<int:pk>/acknowledge/",
         PurchaseViewSet.as_view({"post": "acknowledge"}),),
    path('vendor-performance/<int:vendor_id>/',
         VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]
