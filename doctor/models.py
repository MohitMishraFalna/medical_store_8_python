from department.models import Department
from django.utils import timezone
from django.db import models

# Create your models here.
class Doctor(models.Model):
    # department  = models.ForeignKey(Department, on_delete=models.CASCADE, default=0, null=True,)    
    department  = models.OneToOneField(Department, on_delete=models.CASCADE)    
    name        = models.CharField(max_length=150, default='')
    email       = models.EmailField(max_length=150, default='')
    mobile      = models.CharField(max_length=11, default='')
    created_at  = models.DateField(auto_created=True, default=timezone.now)    
    updated_at  = models.DateField(auto_now_add=True)    
    deleted_at  = models.BooleanField(default=1)

