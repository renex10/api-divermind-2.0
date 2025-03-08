from django.urls import path
from .views import RegistroTerapeuta, RegistroNino,RegistroProfesor  # Importa la clase RegistroNino

urlpatterns = [
path('registros/registro-terapeuta/', RegistroTerapeuta.as_view(), name='registro-terapeuta'),
path('registros/registro-nino/', RegistroNino.as_view(), name='registro-nino'),
path('registros/registro-profesor/', RegistroProfesor.as_view(), name='registro-profesor'),
]

#http://127.0.0.1:8000/api/v1/registros/registro-profesor/

#http://127.0.0.1:8000/api/v1/registros/registro-terapeuta/  