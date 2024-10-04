from rest_framework import serializers
from .models import Branch, Truck


class ValueLabelSerializer(serializers.Serializer):
    value = serializers.UUIDField(source='id')
    label = serializers.CharField(source='name')


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'code', 'created_at', 'updated_at']


class BranchShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', ]


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['id', 'name', 'number', 'code', 'created_at', 'updated_at']


class TruckShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['id', 'name', 'number']