from django.contrib import admin

from employees.models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'truck', 'created_at']
    list_filter = ['truck']
