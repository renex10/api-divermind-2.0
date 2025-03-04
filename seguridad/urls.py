from django.urls import path
from .views import Registro, Verificacion #LoginView  # Importa las vistas necesarias

urlpatterns = [
    # Ruta para el registro de usuarios
    path('registro/', Registro.as_view(), name='registro'),

    # Ruta para la verificación de usuarios mediante un token
    path('verificacion/<str:token>/', Verificacion.as_view(), name='verificacion'),

    # Ruta para el login
    path('login/', LoginView.as_view(), name='login'),
]