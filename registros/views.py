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
    @method_decorator(logueado(rol_requerido='terapeuta'))  # Aplicar el decorador a la vista
    def post(self, request):
        """
        Registra un nuevo niño en el sistema.
        """
        # Verifica si el usuario que realiza la solicitud es un terapeuta
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.rol != 'terapeuta':
                return Response(
                    {"estado": "error", "mensaje": "Solo los terapeutas pueden registrar niños."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except UserProfile.DoesNotExist:
            return Response(
                {"estado": "error", "mensaje": "Perfil de usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Valida los datos del niño
        serializer = NinoSerializer(data=request.data)
        if serializer.is_valid():
            # Asigna el terapeuta al niño
            serializer.save(terapeuta=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Imprime los errores de validación
        print("Errores de validación:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
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
        
 #Vista para Registrar un Niño

#Ahora, crearemos una vista que permita a un terapeuta registrar un niño. Esta vista verificará que el usuario que realiza la solicitud sea un terapeuta.


