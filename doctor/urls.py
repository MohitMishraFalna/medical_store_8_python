from medical_store.auth_middleware import UserAuthenticate
from django.urls import path
from . import views

urlpatterns = [
    path('add/', UserAuthenticate(views.DoctorView.as_view()), name='doctor_add'),
    path('get_doctor_Data/', UserAuthenticate(views.DoctorView.get_doctor_Data), name='get_doctor_Data'),
    path('edit/', UserAuthenticate(views.DoctorView.edit), name='edit_doctor'),
    path('delete/', UserAuthenticate(views.DoctorView.delete), name='delete_doctor'),
    path('doctor_search/', UserAuthenticate(views.DoctorView.doctor_search), name='doctor_search'),

]