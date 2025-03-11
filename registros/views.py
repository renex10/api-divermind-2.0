from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seguridad.decorators import logueado
from seguridad.views import Registro
from .models import Notificacion, SolicitudVinculacion, UserProfile
from .serializers import SolicitudVinculacionSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Nino, UserProfile
from .serializers import NinoSerializer


from rest_framework.response import Response
from rest_framework import status
from seguridad.decorators import logueado
from .models import Nino, UserProfile
from .serializers import NinoSerializer
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from registros import models

from .models import SolicitudVinculacion  # Importar el modelo desde models.py

class RegistroNino(APIView):
    @method_decorator(logueado(rol_requerido='terapeuta'))  # Solo los terapeutas pueden acceder
    def post(self, request):
        """
        Registra un nuevo niño y lo asocia a padres (usuarios con rol "padre").
        """
        # Verifica si el usuario es un terapeuta
        if request.user.profile.rol != 'terapeuta':
            return Response(
                {"estado": "error", "mensaje": "Solo los terapeutas pueden registrar niños."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Valida los datos del niño y los padres
        serializer = NinoSerializer(data=request.data)
        if serializer.is_valid():
            # Asigna automáticamente el terapeuta al niño
            serializer.save(terapeuta=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Si hay errores, devuelve los detalles
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RegistroPadre(Registro):  # Heredar de la clase Registro
    def post(self, request):
        """
        Registra un nuevo padre en el sistema.
        """
        try:
            # Llama al método crear_usuario de la clase padre (Registro)
            usuario, token = self.crear_usuario(request)
            
            # Asigna el rol de padre al usuario
            user_profile = UserProfile.objects.create(user=usuario, rol='padre')
            
            # Serializa el perfil de usuario para la respuesta
            serializer = UserProfileSerializer(user_profile)
            
            # Retorna una respuesta personalizada
            return Response({
                "estado": "éxito",
                "mensaje": "Padre registrado correctamente",
                "perfil": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class RegistroTerapeuta(Registro):
    def post(self, request):
        """
        Registra un nuevo terapeuta en el sistema.
        """
        try:
            # Llama al método crear_usuario de la vista padre
            usuario, token = self.crear_usuario(request)
            
            # Asigna el rol de terapeuta al usuario
            user_profile = UserProfile.objects.create(user=usuario, rol='terapeuta')
            
            # Serializa el perfil de usuario para la respuesta
            serializer = UserProfileSerializer(user_profile)
            
            # Retorna una respuesta personalizada
            return Response({
                "estado": "éxito",
                "mensaje": "Terapeuta registrado correctamente",
                "perfil": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class RegistroProfesor(Registro):  # Heredar de la clase Registro
    def post(self, request):
        """
        Registra un nuevo profesor en el sistema.
        """
        try:
            # Llama al método crear_usuario de la clase padre (Registro)
            usuario, token = self.crear_usuario(request)
            
            # Asigna el rol de profesor al usuario
            user_profile = UserProfile.objects.create(user=usuario, rol='profesor')
            
            # Serializa el perfil de usuario para la respuesta
            serializer = UserProfileSerializer(user_profile)
            
            # Retorna una respuesta personalizada
            return Response({
                "estado": "éxito",
                "mensaje": "Profesor registrado correctamente",
                "perfil": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

#Esta vista permitirá a los profesores enviar solicitudes de vinculación.
# Vista para enviar solicitudes de vinculación
class EnviarSolicitudVinculacion(APIView):
    @method_decorator(logueado(rol_requerido='profesor'))  # Solo los profesores pueden enviar solicitudes
    def post(self, request):
        """
        Envía una solicitud de vinculación para acceder a un niño.
        """
        try:
            # Obtener el ID del niño desde el cuerpo de la solicitud
            nino_id = request.data.get('nino_id')
            
            # Verificar que el niño exista
            nino = Nino.objects.get(id=nino_id)
            
            # Crear la solicitud de vinculación
            solicitud = SolicitudVinculacion.objects.create(
                profesor=request.user,  # Profesor que envía la solicitud (usuario autenticado)
                nino=nino,              # Niño al que se solicita acceso
                estado='pendiente'      # Estado inicial de la solicitud
            )
            
            # Crear una notificación para el terapeuta
            mensaje = f"El profesor {request.user.username} ha solicitado acceso a {nino.nombre}."
            Notificacion.objects.create(
                usuario=nino.terapeuta,  # Terapeuta asociado al niño
                mensaje=mensaje
            )
            
            # Serializar la solicitud para la respuesta
            serializer = SolicitudVinculacionSerializer(solicitud)
            
            # Retornar una respuesta de éxito
            return Response({
                "estado": "éxito",
                "mensaje": "Solicitud de vinculación enviada correctamente",
                "solicitud": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Nino.DoesNotExist:
            # Si el niño no existe, retornar un error 404
            return Response({"estado": "error", "mensaje": "El niño no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Si ocurre un error inesperado, retornar un error 400
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#Vista AprobarSolicitudVinculacion

#Crea una vista para que el terapeuta apruebe o rechace las solicitudes de vinculación:

class AprobarSolicitudVinculacion(APIView):
    @method_decorator(logueado(rol_requerido='terapeuta'))  # Solo los terapeutas pueden aprobar solicitudes
    def post(self, request):
        """
        Aprueba o rechaza una solicitud de vinculación.
        """
        try:
            # Obtener el ID de la solicitud y el nuevo estado desde el cuerpo de la solicitud
            solicitud_id = request.data.get('solicitud_id')
            nuevo_estado = request.data.get('estado')  # 'aprobada' o 'rechazada'

            # Verificar que la solicitud exista y esté pendiente
            solicitud = SolicitudVinculacion.objects.get(id=solicitud_id, estado='pendiente')

            # Actualizar el estado de la solicitud
            solicitud.estado = nuevo_estado
            solicitud.save()

            # Crear una notificación para los padres si la solicitud es aprobada
            if nuevo_estado == 'aprobada':
                mensaje = f"El terapeuta ha aprobado la solicitud de acceso a {solicitud.nino.nombre}."
                Notificacion.objects.create(
                    usuario=solicitud.nino.padres.first(),  # Notificar al primer padre
                    mensaje=mensaje
                )

            # Retornar una respuesta de éxito
            return Response({
                "estado": "éxito",
                "mensaje": f"Solicitud {nuevo_estado} correctamente",
                "solicitud": SolicitudVinculacionSerializer(solicitud).data
            }, status=status.HTTP_200_OK)
        
        except SolicitudVinculacion.DoesNotExist:
            return Response({"estado": "error", "mensaje": "La solicitud no existe o ya fue procesada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# Consentimiento de los Padres
#Vista ConsentimientoPadre

#Crea una vista para que los padres den su consentimiento o rechacen la solicitud:

class ConsentimientoPadre(APIView):
    @method_decorator(logueado(rol_requerido='padre'))  # Solo los padres pueden dar consentimiento
    def post(self, request):
        """
        Da consentimiento o rechaza una solicitud de vinculación.
        """
        try:
            # Obtener el ID de la solicitud y la decisión desde el cuerpo de la solicitud
            solicitud_id = request.data.get('solicitud_id')
            decision = request.data.get('decision')  # 'aprobada' o 'rechazada'

            # Validar la decisión
            if decision not in ['aprobada', 'rechazada']:
                return Response({
                    "estado": "error",
                    "mensaje": "La decisión debe ser 'aprobada' o 'rechazada'."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que la solicitud exista y esté aprobada por el terapeuta
            solicitud = SolicitudVinculacion.objects.get(id=solicitud_id, estado='aprobada')

            # Actualizar el estado de la solicitud según la decisión del padre
            if decision == 'aprobada':
                solicitud.estado = 'consentida'
            else:
                solicitud.estado = 'rechazada'
            solicitud.save()

            # Crear una notificación para el profesor
            mensaje_profesor = f"El padre ha {decision} la solicitud de acceso a {solicitud.nino.nombre}."
            Notificacion.objects.create(
                usuario=solicitud.profesor,
                mensaje=mensaje_profesor
            )

            # Crear una notificación para el padre
            mensaje_padre = f"Has {decision} la solicitud de acceso a {solicitud.nino.nombre}."
            Notificacion.objects.create(
                usuario=request.user,  # El padre que está dando el consentimiento
                mensaje=mensaje_padre
            )

            # Retornar una respuesta de éxito
            return Response({
                "estado": "éxito",
                "mensaje": f"Solicitud {decision} por el padre",
                "solicitud": SolicitudVinculacionSerializer(solicitud).data
            }, status=status.HTTP_200_OK)
        
        except SolicitudVinculacion.DoesNotExist:
            return Response({
                "estado": "error",
                "mensaje": "La solicitud no existe o no está aprobada por el terapeuta."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "estado": "error",
                "mensaje": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class VerNotificaciones(APIView):
    @method_decorator(logueado(rol_requerido='terapeuta'))  # Solo los terapeutas pueden ver notificaciones
    def get(self, request):
        """
        Obtiene las notificaciones del terapeuta.
        """
        try:
            # Obtener las notificaciones del terapeuta
            notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
            
            # Serializar las notificaciones para la respuesta
            notificaciones_data = [{
                "id": notificacion.id,
                "mensaje": notificacion.mensaje,
                "fecha": notificacion.fecha
            } for notificacion in notificaciones]
            
            # Retornar una respuesta de éxito
            return Response({
                "estado": "éxito",
                "notificaciones": notificaciones_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Si ocurre un error inesperado, retornar un error 400
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class VerNotificaciones(APIView):
    @method_decorator(logueado(rol_requerido='terapeuta'))  # Solo los terapeutas pueden ver notificaciones
    def get(self, request):
        """
        Obtiene las notificaciones del terapeuta.
        """
        try:
            # Obtener las notificaciones del terapeuta que no han sido leídas
            notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
            
            # Serializar las notificaciones para la respuesta
            notificaciones_data = [{
                "id": notificacion.id,
                "mensaje": notificacion.mensaje,
                "fecha": notificacion.fecha.strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # Formato ISO 8601
            } for notificacion in notificaciones]
            
            # Retornar una respuesta de éxito
            return Response({
                "estado": "éxito",
                "notificaciones": notificaciones_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Si ocurre un error inesperado, retornar un error 400
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)

