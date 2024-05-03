from rest_framework import serializers
from .models import Vendor, Performance, Purchase

# Your serializer code here


# Your serializer code here


class Venderserializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class Purchaseserialiazer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class Performanceserializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"
