from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, StatisticsView

router = DefaultRouter()
router.register('', InventoryViewSet)
# router.register(r'inventory-actions', InventoryActionViewSet)
# router.register(r'inventory-images', InventoryImageViewSet)

urlpatterns = [
    path('statistics/', StatisticsView.as_view(), name='statistics'),


    path('', include(router.urls)),
]
