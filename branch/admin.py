from django.contrib import admin

from .models import Branch, Truck


@admin.register(Branch)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", 'code', 'address', 'created_at')
    search_fields = ("name", 'code', 'address')


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("name", 'number', 'code', 'created_at')
    search_fields = ("name", 'number', 'code')