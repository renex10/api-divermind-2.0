from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('seguridad.urls')),  # URLs de "seguridad"
    path('api/v1/', include('registros.urls')),  # URLs de "registros"
]