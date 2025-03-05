from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('seguridad.urls')),  # Prefijo api/v1/ para las URLs de "seguridad"
]