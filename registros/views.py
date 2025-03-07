from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seguridad.views import Registro
from .models import UserProfile
from .serializers import UserProfileSerializer

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