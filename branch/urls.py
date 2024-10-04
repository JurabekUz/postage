from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, TruckViewSet

router = DefaultRouter()
router.register(r'', BranchViewSet)
router.register(r'trucks', TruckViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
