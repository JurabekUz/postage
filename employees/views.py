from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Driver
from .serializers import DriverSerializer, DriverShortSerializer


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all().select_related('truck')
    serializer_class = DriverSerializer

    @extend_schema(
        responses=DriverShortSerializer
    )
    @action(detail=False, methods=['get'])
    def short(self, request):
        slz = DriverShortSerializer(self.get_queryset(), many=True)
        return Response(slz.data)
