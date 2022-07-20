from department.models import Department
from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name                = models.CharField(max_length=150, default='')
    department          = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='departments')
    amt                 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity            = models.IntegerField(default=0)
    manufacturing       = models.DateField(auto_created=True, default=timezone.now)
    expiry              = models.DateField(auto_created=True, default=timezone.now)
    created_at          = models.DateField(auto_created=True, default=timezone.now)
    updated_at          = models.DateField(auto_now_add=True)
    deleted_at          = models.BooleanField(default=1)