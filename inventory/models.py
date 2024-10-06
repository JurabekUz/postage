from django.db import models
from django.utils.translation import gettext_lazy as _

from branch.models import Branch
from employees.models import Driver
from utils.abstract_models import BaseModel


class Status(models.IntegerChoices):
    accepted = 1, _('Accepted')
    sent = 2, _('Sent')
    delivered = 3, _('Delivered')
    closed = 4, _('Closed')


class Inventory(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventories')
    number = models.CharField(max_length=20, editable=False)
    order_number = models.PositiveIntegerField(editable=False)
    status = models.IntegerField(choices=Status.choices, default=Status.accepted)
    recipient = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='received_inventories')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='inventories')

    sender_name = models.CharField(max_length=255)
    sender_phone = models.CharField(max_length=20)
    acceptor_name = models.CharField(max_length=255)
    acceptor_phone = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.IntegerField(default=0)
    comment = models.TextField()
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.number:
            order_number = Inventory.objects.aggregate(
                models.Max('order_number', default=0)
            )['order_number__max'] + 1
            formated_number = format_number(order_number)
            self.order_number = order_number
            self.number = formated_number
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")
        db_table = 'inventory'
        ordering = ['-created_at']


    def __str__(self):
        return self.number


class InventoryAction(BaseModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='actions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='actions')
    action = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.accepted)
    send_mgs = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Inventory Action")
        verbose_name_plural = _("Inventory Actions")
        db_table = 'inventory_action'
        ordering = ['action']


class InventoryImage(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='inventory')

    class Meta:
        verbose_name = _("Inventory Image")
        verbose_name_plural = _("Inventory Images")
        db_table = 'inventory_image'


def format_number(number):
    return f"M-{number:05d}"


def reverse_format(formatted_string):
    # Extract the number part from the string and convert it to an integer
    return int(formatted_string.split('-')[1])