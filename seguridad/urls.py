from django.urls import path
from .views import Registro, Verificacion, Login

urlpatterns = [
    # Ruta para el registro de usuarios
    path('seguridad/registro/', Registro.as_view(), name='registro'),

    # Ruta para la verificación de usuarios mediante un token
    path('seguridad/verificacion/<str:token>/', Verificacion.as_view(), name='verificacion'),

    # Ruta para el login de usuarios
    path('seguridad/login/', Login.as_view(), name='login'),
]

#http://127.0.0.1:8000/api/v1/registros/registro-nino/
#http://127.0.0.1:8000/api/v1/seguridad/login/