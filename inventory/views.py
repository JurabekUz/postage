from django.db import transaction
from django.db.models import Q, Count, Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from branch.models import Branch
from employees.models import Driver
from users.models import BotUser
from utils.filters import InventoryFilter
from utils.msg_services import send_telegram_message
from .models import Inventory, InventoryAction, Status
from .serializers import (
    InventoryListSerializer, InventoryCreateSerializer, InventoryDetailSerializer
)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryListSerializer
    filterset_class = InventoryFilter
    search_fields = ['acceptor_name', 'sender_name']

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
        try:
            tg_id = BotUser.objects.get(phone_number=obj.sender_phone).telegram_id
            send_telegram_message(tg_id, obj)
        except BotUser.DoesNotExist:
            print('BotUser does not exist')
        except Exception as err:
            print(err)
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
        try:
            tg_id = BotUser.objects.get(phone_number=obj.sender_phone).telegram_id
            send_telegram_message(tg_id, obj)
            tg_id_2 = BotUser.objects.get(phone_number=obj.acceptor_phone).telegram_id
            send_telegram_message(tg_id_2, obj)
        except BotUser.DoesNotExist:
            print('BotUser does not exist')
        except Exception as err:
            print(err)
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
        try:
            tg_id = BotUser.objects.get(phone_number=obj.sender_phone).telegram_id
            send_telegram_message(tg_id, obj)
            tg_id_2 = BotUser.objects.get(phone_number=obj.acceptor_phone).telegram_id
            send_telegram_message(tg_id_2, obj)
        except BotUser.DoesNotExist:
            print('BotUser does not exist')
        except Exception as err:
            print(err)
        return Response(status=200)


class StatisticsView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        inv = Inventory.objects.all()
        if year:
            inv = inv.filter(created_at__year=int(year))

        all_count = inv
        accepted_count = inv.filter(status=Status.accepted)
        sent_count = inv.filter(status=Status.sent)
        delivered_count = inv.filter(status=Status.delivered)
        closed_count = inv.filter(status=Status.closed)


        if not self.request.user.is_staff:
            all_count = all_count.filter(
                Q(branch_id=self.request.user.branch_id) | Q(recipient_id=self.request.user.branch_id)
            )
            accepted_count = accepted_count.filter(branch_id=self.request.user.branch_id)
            sent_count = sent_count.filter(
                Q(branch_id=self.request.user.branch_id) | Q(recipient_id=self.request.user.branch_id)
            )
            delivered_count = delivered_count.filter(recipient_id=self.request.user.branch_id)
            closed_count = closed_count.filter(recipient_id=self.request.user.branch_id)

            inv = inv.filter(
                Q(branch_id=self.request.user.branch_id) | Q(recipient_id=self.request.user.branch_id)
            )

        monthly_stat_counts = inv.annotate(
            month=ExtractMonth('created_at')
        ).values('month').annotate(
            count=Count('id'),
            total_weight=Sum('weight'),
            total_price=Sum('price')
        ).order_by('month')

        monthly_counts = [0] * 12
        monthly_weights = [0] * 12
        monthly_prices = [0] * 12

        for item in monthly_stat_counts:
            monthly_counts[item['month'] - 1] = item['count']
            monthly_weights[item['month'] - 1] = item['total_weight']
            monthly_prices[item['month'] - 1] = item['total_price']

        stat = {
            "all_count": all_count.aggregate(count=Count('id'))['count'],
            'accepted': accepted_count.aggregate(count=Count('id'))['count'],
            'sent': sent_count.aggregate(count=Count('id'))['count'],
            'delivered': delivered_count.aggregate(count=Count('id'))['count'],
            'closed': closed_count.aggregate(count=Count('id'))['count'],
            'monthly_counts': monthly_counts,
            'monthly_weights': monthly_weights,
            'monthly_prices': monthly_prices
        }

        return Response(data=stat)
