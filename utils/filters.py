from inventory.models import Inventory
from django_filters import rest_framework as filters


class InventoryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='created_at', lookup_expr='date')

    class Meta:
        model = Inventory
        fields = ['status', 'recipient', 'date', 'number', 'is_paid']
