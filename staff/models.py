from django.utils import timezone
from django.db import models



# Create your models here.

class Staff(models.Model):
    first_name      =    models.CharField(max_length=150, default='')
    last_name       =    models.CharField(max_length=150, default='')
    email           =    models.EmailField(unique=True)
    username        =    models.CharField(max_length=150, default='', unique=True)
    password        =    models.CharField(max_length=254, default='')
    dob             =    models.DateField(default=timezone.now)
    gender          =    models.CharField(max_length=6, choices=[('Male', 'Male'),('Female', 'Female')])
    mobile          =    models.IntegerField(default=0)
    profile_img     =    models.ImageField(upload_to='profileImage/', default='profileImage/profile-img.jpg')
    pincode         =    models.IntegerField(default=0)
    city            =    models.CharField( max_length=150, default='')
    dist            =    models.CharField(max_length=150, default='')
    state           =    models.CharField( max_length=150, default='')
    country         =    models.CharField(max_length=150, default='')
    about_user      =    models.CharField(max_length=250, default='')
    user_role       =    models.CharField(max_length=30, choices=[('Owner', 'Owner'), ('Seller', 'Seller')])
    login_attempt   =    models.IntegerField(default=0)
    pwd_reset       =    models.BooleanField(default=0)
    deleted_at      =    models.BooleanField(default=1)
    created_at      =    models.DateTimeField(auto_now_add=True)
    updated_at      =    models.DateTimeField(auto_now_add=True)
    # created_at      =    models.DateTimeField(default=timezone.now)
    # updated_at      =    models.DateTimeField(default=timezone.now)
