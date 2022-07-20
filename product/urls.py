from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    path('add/', UserAuthenticate(views.ProductView.as_view()), name='new_product'),
    path('get_product_Data/', UserAuthenticate(views.ProductView.get_product_Data), name='get_product_Data'),
    path('edit/', UserAuthenticate(views.ProductView.edit), name='edit_product'),
    path('delete/', UserAuthenticate(views.ProductView.delete), name='delete_product'),
    path('product_search/', UserAuthenticate(views.ProductView.product_search), name='product_search'),
]