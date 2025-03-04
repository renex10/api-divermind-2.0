from django.urls import path
from .views import Registro, Verificacion

urlpatterns = [
    # Ruta para el registro de usuarios
    path('registro/', Registro.as_view(), name='registro'),

    # Ruta para la verificación de usuarios mediante un token
    path('verificacion/<str:token>/', Verificacion.as_view(), name='verificacion'),


]