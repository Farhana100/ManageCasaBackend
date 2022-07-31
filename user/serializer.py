from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'
