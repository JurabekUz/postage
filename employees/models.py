from django.db import models

from branch.models import Branch, Truck
from utils.abstract_models import BaseModel
from django.utils.translation import gettext_lazy as _


class Driver(BaseModel):
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='drivers')
    name = models.CharField(max_length=255)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='drivers')

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")
        db_table = 'driver'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
