""" ruta apidivermind.urls """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('seguridad.urls')),  # Incluye las URLs de la aplicación "seguridad"
]