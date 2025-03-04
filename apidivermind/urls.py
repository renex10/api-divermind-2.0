from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('api/v1/', include('seguridad.urls')),  # Incluye las rutas de la aplicación 'seguridad'
]