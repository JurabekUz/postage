from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from branch.models import Branch
from employees.models import Driver
from utils.filters import InventoryFilter
from .models import Inventory, InventoryAction, Status
from .serializers import (
    InventoryListSerializer, InventoryCreateSerializer, InventoryDetailSerializer
)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryListSerializer
    filterset_class = InventoryFilter
    search_fields = ['acceptor_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InventoryDetailSerializer
        if self.action == 'create':
            return InventoryCreateSerializer
        return InventoryListSerializer

    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status')
        in_way = self.request.query_params.get('inWay')
        if self.action == 'retrieve':
            queryset = queryset.select_related('branch', 'recipient').prefetch_related('images')
        elif not self.request.user.is_staff:
            if in_way == 'true':
                queryset = queryset.filter(recipient=self.request.user.branch_id, status=Status.sent)
            elif status:
                if int(status) in [Status.delivered, Status.closed]:
                    queryset = queryset.filter(recipient_id=self.request.user.branch_id)
                else:
                    queryset = queryset.filter(branch_id=self.request.user.branch_id)
            else:
                queryset = queryset.filter(
                    Q(branch_id=self.request.user.branch_id) | Q(recipient_id=self.request.user.branch_id)
                )
        return queryset

    @extend_schema(description='data = {"recipient": id}')
    @action(detail=True, methods=['post'], url_path='send')
    def action_sent(self, request, pk):
        obj = self.get_object()

        recipient = get_object_or_404(Branch, id=self.request.data.get('recipient'))
        driver = get_object_or_404(Driver, id=self.request.data.get('driver'))

        with transaction.atomic():
            obj.status = Status.sent
            obj.recipient = recipient
            obj.driver = driver
            obj.save()

            InventoryAction.objects.create(
                inventory=obj,
                user=self.request.user,
                action=Status.sent
            )

        return Response(status=200)

    @action(detail=True, methods=['post'], url_path='deliver')
    def action_delivered(self, request, pk):
        obj = self.get_object()
        with transaction.atomic():
            obj.status = Status.delivered
            obj.save()

            InventoryAction.objects.create(
                inventory=obj,
                user=self.request.user,
                action=Status.delivered
            )
        return Response(status=200)

    @action(detail=True, methods=['post'], url_path='close')
    def action_closed(self, request, pk):
        obj = self.get_object()
        with transaction.atomic():
            obj.status = Status.closed
            obj.is_paid = True
            obj.save()

            InventoryAction.objects.create(
                inventory=obj,
                user=self.request.user,
                action=Status.closed
            )
        return Response(status=200)
