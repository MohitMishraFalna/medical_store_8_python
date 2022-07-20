from product.models import Product
from django.utils import timezone
from doctor.models import Doctor
from django.db import models

# Create your models here.
# Customer
class Customer(models.Model):
    doctor_id   = models.CharField(max_length=50, default='')
    name        = models.CharField(max_length=150, default='')
    mobile      = models.EmailField(max_length=150, default='')
    due_amt     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at  = models.DateField(auto_created=True, default=timezone.now)
    updated_at  = models.DateField(auto_now_add=True)
    deleted_at  = models.BooleanField(default=1) 

class Order(models.Model):
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    doctor          = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctors')
    order_date      = models.DateField(auto_created=True, default=timezone.now)
    bill_amt        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst             = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total_amt       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amt         = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    payable_amt     = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    paid_amt        = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    payment_data    = models.TextField(default='')
    payment_status  = models.CharField(max_length=20, default='')
    created_at      = models.DateField(auto_created=True, default=timezone.now)
    updated_at      = models.DateField(auto_now_add=True)
    deleted_at      = models.BooleanField(default=1) 

class ProductOrder(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    order_qty    = models.IntegerField(default=0)
    # total_amt    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at   = models.DateField(auto_created=True, default=timezone.now)
    updated_at   = models.DateField(auto_now_add=True)
    deleted_at   = models.BooleanField(default=1) 




