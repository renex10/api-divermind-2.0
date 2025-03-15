from django.urls import path

from seguridad.views import GenerarTokenTerapeuta
from .views import AprobarSolicitudVinculacion, ConsentimientoPadre, EnviarSolicitudVinculacion, RegistroAdministrador, RegistroTerapeuta, RegistroNino,RegistroProfesor,RegistroPadre, VerNotificaciones  # Importa la clase RegistroNino

urlpatterns = [
path('registros/registro-administrador/', RegistroAdministrador.as_view(), name='registro-administrador'),
 path('registros/generar-token/', GenerarTokenTerapeuta.as_view(), name='generar-token'),
path('registros/registro-terapeuta/', RegistroTerapeuta.as_view(), name='registro-terapeuta'),
path('registros/registro-nino/', RegistroNino.as_view(), name='registro-nino'),
path('registros/registro-profesor/', RegistroProfesor.as_view(), name='registro-profesor'),
 path('registros/registro-padre/', RegistroPadre.as_view(), name='registro-padre'),
path('registros/solicitud-vinculacion/', EnviarSolicitudVinculacion.as_view(), name='solicitud-vinculacion'),
 path('registros/notificaciones/', VerNotificaciones.as_view(), name='ver-notificaciones'), #en postma con metodo GET: http://127.0.0.1:8000/api/v1/registros/notificaciones/
    # Ruta para aprobar/rechazar solicitudes de vinculación
path('registros/aprobar-solicitud/', AprobarSolicitudVinculacion.as_view(), name='aprobar-solicitud'),
  
     # Ruta para dar consentimiento o rechazar solicitudes
path('registros/consentimiento/', ConsentimientoPadre.as_view(), name='consentimiento'),
      
]
#http://127.0.0.1:8000/api/v1/registros/consentimiento/
#http://127.0.0.1:8000/api/v1/registros/notificaciones/
#http://127.0.0.1:8000/api/v1/registros/aprobar-solicitud/
#http://127.0.0.1:8000/api/v1/registros/consentimiento/
#http://127.0.0.1:8000/api/v1/registros/solicitud-vinculacion/
#http://127.0.0.1:8000/api/v1/registros/registro-profesor/

#http://127.0.0.1:8000/api/v1/registros/registro-terapeuta/  