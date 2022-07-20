from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('staff.urls')),
    path('owner/', include('owner.urls')),
    path('seller/', include('seller.urls')),
    path('department/', include('department.urls')),
    path('doctor/', include('doctor.urls')),
    path('customer/', include('customer.urls')),
    path('product/', include('product.urls'))
]
