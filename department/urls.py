# Import our custome middleware file here
from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    path('new_department/', UserAuthenticate(views.DepartmentView.as_view()), name='new_department'),
    path('get_department_Data/', UserAuthenticate(views.DepartmentView.get_department_Data), name='get_department_Data'),
    path('edit/', UserAuthenticate(views.DepartmentView.edit), name='edit_department'),
    path('delete/', UserAuthenticate(views.DepartmentView.delete), name='delete_department'),
    path('department_search/', UserAuthenticate(views.DepartmentView.department_search), name='department_search'),
]