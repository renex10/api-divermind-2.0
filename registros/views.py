from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seguridad.views import Registro
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Nino, UserProfile
from .serializers import NinoSerializer

class RegistroNino(APIView):
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


class RegistroNino(APIView):
    def post(self, request):
        """
        Registra un nuevo niño en el sistema.
        """
        # Obtener el correo del terapeuta desde la solicitud
        correo_terapeuta = request.data.get("correo_terapeuta")
        if not correo_terapeuta:
            return Response(
                {"estado": "error", "mensaje": "El campo 'correo_terapeuta' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si el terapeuta existe y está activo
        try:
            terapeuta = User.objects.get(email=correo_terapeuta, is_active=True)
            user_profile = UserProfile.objects.get(user=terapeuta)
            if user_profile.rol != 'terapeuta':
                return Response(
                    {"estado": "error", "mensaje": "El usuario no es un terapeuta."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response(
                {"estado": "error", "mensaje": "Terapeuta no encontrado o no está activo."},
                status=status.HTTP_404_NOT_FOUND
            )
        except UserProfile.DoesNotExist:
            return Response(
                {"estado": "error", "mensaje": "Perfil de terapeuta no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Valida los datos del niño
        serializer = NinoSerializer(data=request.data)
        if serializer.is_valid():
            # Asigna el terapeuta al niño
            serializer.save(terapeuta=terapeuta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)