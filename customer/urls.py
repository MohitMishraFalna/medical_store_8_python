from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    # path('add/', UserAuthenticate(views.DepartmentView.as_view()), name='new_department'),
]