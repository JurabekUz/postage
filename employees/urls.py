from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employees.views import DriverViewSet

router = DefaultRouter()
router.register('drivers', DriverViewSet, basename='driver')

urlpatterns = [
    path('', include(router.urls))
]