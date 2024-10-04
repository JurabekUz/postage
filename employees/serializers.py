from rest_framework import serializers

from branch.serializers import TruckShortSerializer
from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    truck = TruckShortSerializer(allow_null=True)

    class Meta:
        model = Driver
        fields = ['id', 'name', 'truck']


class DriverShortSerializer(serializers.Serializer):
    value = serializers.UUIDField(source='id')
    label = serializers.CharField(source='name')
    truck_name = serializers.CharField(source='truck.name')
    truck_number = serializers.CharField(source='truck.number')
