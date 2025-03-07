from django.urls import path
from .views import RegistroTerapeuta

urlpatterns = [
    path('registros/registro-terapeuta/', RegistroTerapeuta.as_view(), name='registro-terapeuta'),
]