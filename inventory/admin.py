from django.contrib import admin

from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'acceptor_name', 'weight', 'status', 'number', 'is_paid']
    list_filter = ['status', 'is_paid', 'number']
