from django.db import models

# Create your models here.
class Department(models.Model):
    name        = models.CharField(max_length=50, default='')
    created_at  = models.DateField(auto_now_add=True)    
    updated_at  = models.DateField(auto_now_add=True)    
    deleted_at  = models.BooleanField(default=1)  

    def __str__(self):
        return self.name