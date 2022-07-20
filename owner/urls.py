from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', UserAuthenticate(views.DashboardView.as_view()), name='dashboard'),
    # Department
    path('department_edit/', UserAuthenticate(views.DashboardView.department_edit), name='department_edit'),
    path('department_update/', UserAuthenticate(views.DashboardView.department_update), name='department_update'),
    path('department_delete/', UserAuthenticate(views.DashboardView.department_delete), name='department_delete'),
    
    # Doctor
    path('doctor_edit/', UserAuthenticate(views.DashboardView.doctor_edit), name='doctor_edit'),
    path('doctor_update/', UserAuthenticate(views.DashboardView.doctor_update), name='doctor_update'),
    path('doctor_delete/', UserAuthenticate(views.DashboardView.doctor_delete), name='doctor_delete'),

    # Product
    path('product_edit/', UserAuthenticate(views.DashboardView.product_edit), name='edit_product'),
    path('product_delete/', UserAuthenticate(views.DashboardView.product_delete), name='delete_product'),
    path('product_update/', UserAuthenticate(views.DashboardView.product_update), name='product_update'),

    # Order_Product
    path('order_product_table/', UserAuthenticate(views.DashboardView.order_product_table), name='order_product_table'),
    
    # Search
    path('staff_delete/', UserAuthenticate(views.DashboardView.staff_delete), name='staff_delete'),
    path('staff_search', UserAuthenticate(views.DashboardView.staff_search), name='staff_search'),
    path('new_password/', UserAuthenticate(views.DashboardView.new_password), name='new_password')
]

