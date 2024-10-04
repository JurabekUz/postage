from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet

router = DefaultRouter()
router.register('', InventoryViewSet)
# router.register(r'inventory-actions', InventoryActionViewSet)
# router.register(r'inventory-images', InventoryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
