from django.contrib.auth.models import AbstractUser
from django.db import models

from branch.models import Branch
from django.utils.translation import gettext_lazy as _


# class UserRole(models.TextChoices):
#     admin = 'admin', _('Admin')
#     employee = 'employee', _('Employee')


class User(AbstractUser):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

