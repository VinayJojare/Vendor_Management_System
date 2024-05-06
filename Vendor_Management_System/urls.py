from django.contrib import admin
from django.urls import path, include
from Store.views import *
from rest_framework.authtoken import views

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
    path('api-token-auth/', views.obtain_auth_token),
    path('register', RegisterUserViewSet.as_view()),
]
