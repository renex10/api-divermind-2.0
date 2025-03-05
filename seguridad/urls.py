from django.urls import path
from .views import Registro, Verificacion

urlpatterns = [
    path('api/v1/seguridad/registro/', Registro.as_view(), name='registro'),
    path('api/v1/seguridad/verificacion/<str:token>/', Verificacion.as_view(), name='verificacion'),
]