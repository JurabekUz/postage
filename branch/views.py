from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Branch, Truck
from .serializers import BranchSerializer, TruckSerializer, BranchShortSerializer, ValueLabelSerializer


# Branch ViewSet
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    @extend_schema(
        responses=ValueLabelSerializer,
        description='[{"value": id, "label": name}]'
    )
    @action(detail=False, methods=['get'])
    def short(self, request):
        queryset = self.get_queryset().exclude(id=request.user.branch_id)
        serializer = ValueLabelSerializer(queryset, many=True)
        return Response(serializer.data)


# Truck ViewSet
class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    @action(detail=False, methods=['get'])
    def short(self, request):
        queryset = self.queryset.values('id', 'name', 'number')
        return Response(queryset)
