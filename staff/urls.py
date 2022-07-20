# Import our custome middleware file here
from medical_store.auth_middleware import UserAuthenticate
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('register/', UserAuthenticate(views.RegisterView.as_view()), name='register'),
    path('reset/', UserAuthenticate(views.ResetPassword.as_view()), name='reset_password'),
    # both url are same but one for using redirect the page and second for using by click link and reach the page.
    path('profile/', UserAuthenticate(views.ProfileView.as_view()), name='profile'),
    path('profile/<eml>', views.ProfileView.as_view(), name='profile'),
    path('getAddress/', UserAuthenticate(views.getAddress), name='address'),
    path('logout/', UserAuthenticate(views.logout), name='logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)