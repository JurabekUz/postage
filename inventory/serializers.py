from django.db import transaction
from rest_framework import serializers

from employees.serializers import DriverSerializer
from users.serializers import UserFullNameSerializer
from utils.msg_services import generate_msg, send_telegram_message
from .models import Inventory, InventoryAction, InventoryImage, Status
from users.models import BotUser


class IdNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class InventoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryImage
        fields = ['image', 'id']


class InventoryActionSerializer(serializers.ModelSerializer):
    user = UserFullNameSerializer()

    class Meta:
        model = InventoryAction
        fields = ['id', 'user', 'action']


class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'sender_name', 'sender_phone', 'acceptor_name', 'acceptor_phone', 'weight', 'price', 'comment', 'is_paid', 'number'
        ]
        extra_kwargs = {
            'number': {'read_only': True}
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data['branch'] = self.context['request'].user.branch
        obj = super().create(validated_data)

        InventoryAction.objects.create(
            inventory=obj,
            user=self.context['request'].user,
            action=Status.accepted
        )

        for image in self.context['request'].FILES.getlist('images'):
            InventoryImage.objects.create(inventory=obj, image=image)

        try:
            tg_id = BotUser.objects.get(phone_number=validated_data['sender_phone']).telegram_id
            send_telegram_message(tg_id, obj)
        except BotUser.DoesNotExist:
            print('BotUser does not exist')
        except Exception as err:
            print(err)
        return obj


class InventoryListSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(source='recipient.name', allow_null=True)
    branch = serializers.CharField(source='branch.name', allow_null=True)

    class Meta:
        model = Inventory
        fields = ['id', 'branch', 'sender_name', 'acceptor_name', 'weight', 'status', 'number', 'recipient', 'is_paid']


class InventoryDetailSerializer(serializers.ModelSerializer):
    recipient = IdNameSerializer()
    branch = IdNameSerializer()
    driver = DriverSerializer()
    images = InventoryImageSerializer(many=True)
    # actions = InventoryActionSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        to_rep = super().to_representation(instance)
        sent = instance.actions.filter(action=Status.sent).last()
        delivered = instance.actions.filter(action=Status.delivered).last()
        closed = instance.actions.filter(action=Status.closed).last()
        to_rep['sent_at'] = sent.created_at.strftime("%d.%m.%Y %H:%M") if sent else None
        to_rep['delivered_at'] = delivered.created_at.strftime("%d.%m.%Y %H:%M") if delivered else None
        to_rep['closed_at'] = closed.created_at.strftime("%d.%m.%Y %H:%M") if closed else None
        return to_rep
