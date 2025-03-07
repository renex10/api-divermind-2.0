from django.urls import path
from .views import RegistroTerapeuta, RegistroNino

urlpatterns = [
    path('registros/registro-terapeuta/', RegistroTerapeuta.as_view(), name='registro-terapeuta'),
    path('registros/registro-nino/', RegistroNino.as_view(), name='registro-nino'),
]