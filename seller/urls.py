from django import views
from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    path('workbench/', UserAuthenticate(views.NewBill.as_view()), name='workbench'),
    path('customer_exists/', UserAuthenticate(views.NewBill.customer_exists), name='customer_exist'),
    path('doctor_exists/', UserAuthenticate(views.NewBill.doctor_exists), name='doctor_exist'),
    path('product_list/', UserAuthenticate(views.NewBill.product_list), name='product_list'),
    path('save_payemnt_status/', UserAuthenticate(views.NewBill.save_payemnt_status), name='save_payemnt_status')
]