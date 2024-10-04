from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstract_models import BaseModel


class Branch(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    address = models.CharField(max_length=500, verbose_name=_("Address"))
    code = models.PositiveSmallIntegerField(unique=True, editable=False, verbose_name=_("Code"))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Branch.objects.aggregate(models.Max('code', default=0))['code__max'] + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")
        db_table = 'Branch'
        ordering = ['-created_at']



    def __str__(self):
        return self.name


class Truck(BaseModel):
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='trucks', verbose_name=_("Branch"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    number = models.CharField(max_length=20, verbose_name=_("Number"))
    code = models.PositiveSmallIntegerField(unique=True, editable=False, verbose_name=_("Code"))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Truck.objects.aggregate(models.Max('code', default=0))['code__max'] + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Truck")
        verbose_name_plural = _("Trucks")
        db_table = 'Truck'
        ordering = ['-created_at']

    def __str__(self):
        return self.name