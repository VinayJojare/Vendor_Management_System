from rest_framework import serializers
from .models import Vendor, Performance, Purchase
from django.contrib.auth.models import User


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


class UserSerialazer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
