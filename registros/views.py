from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seguridad.decorators import logueado
from seguridad.views import Registro
from .models import UserProfile
from .serializers import UserProfileSerializer
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




