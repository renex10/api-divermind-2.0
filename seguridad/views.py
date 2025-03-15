# ruta de este archivo es: seguridad\views.py
from django.shortcuts import render
from registros.models import UserProfile
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponseRedirect
from http import HTTPStatus
import os
import uuid
from dotenv import load_dotenv
from django.contrib.auth.models import User
from .models import UsersMetadata
from utilidades import utilidades
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
import time
from jose import jwt

# Carga las variables de entorno desde un archivo .env
load_dotenv()

class Registro(APIView):
    def crear_usuario(self, request):
        """
        Método para crear un usuario y generar un token.
        Retorna el usuario creado y el token.
        """
        try:
            # Crea un nuevo usuario
            u = User.objects.create_user(
                username=request.data["nombre"],
                email=request.data["correo"],
                password=request.data["password"],
                is_active=False
            )
            
            # Genera un token único
            token = str(uuid.uuid4())
            UsersMetadata.objects.create(token=token, user=u)
            
            # Envía el correo de verificación
            url = f"{os.getenv('base_URL')}/api/v1/seguridad/verificacion/{token}"
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #e0e0e0;
                        display: flex;
                        justify-content: center;
                    }}
                    .container {{
                        background: #e0e0e0;
                        border-radius: 20px;
                        box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
                        padding: 20px;
                        text-align: center;
                        max-width: 500px;
                        margin: auto;
                    }}
                    h3 {{
                        color: #333;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }}
                    p {{
                        color: #555;
                        font-size: 18px;
                        margin-bottom: 20px;
                    }}
                    a {{
                        display: inline-block;
                        background-color: #007bff;
                        color: #fff;
                        padding: 10px 20px;
                        border-radius: 10px;
                        text-decoration: none;
                        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
                    }}
                    a:hover {{
                        background-color: #0056b3;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h3>Verificación de cuenta</h3>
                    <p>Hola {request.data["nombre"]}, te has registrado exitosamente. Para activar tu cuenta, haz clic en el enlace:</p>
                    <a href="{url}">Aquí</a>
                    <p>O copia y pega la siguiente URL en tu navegador favorito:</p>
                    <p>{url}</p>
                </div>
            </body>
            </html>
            """
            utilidades.sendMail(html, "verificacion", request.data["correo"])
            
            return u, token
        
        except Exception as e:
            raise Exception(f"Ocurrió un error inesperado: {str(e)}")

    def post(self, request):
        """
        Maneja las solicitudes POST para registrar un nuevo usuario.
        """
        # Verifica si los campos obligatorios están presentes
        if not all([request.data.get("nombre"), request.data.get("correo"), request.data.get("password")]):
            return JsonResponse({"estado": "error", "mensaje": "Todos los campos son obligatorios"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            # Crea el usuario y genera el token
            usuario, token = self.crear_usuario(request)
            
            # Retorna una respuesta de éxito
            return JsonResponse({"estado": "éxito", "mensaje": "Registro exitoso", "token": token}, status=HTTPStatus.OK)
        
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": str(e)}, status=HTTPStatus.BAD_REQUEST)
        
        
class Verificacion(APIView):
    def get(self, request, token):
        # Verificar si el token es None o está vacío
        if token is None or not token:
            return JsonResponse(
                {"estado": "error", "mensaje": "recurso no disponible"},
                status=404
            )
        
        try:
            # Buscar en UsersMetadata el registro que contenga el token
            data = UsersMetadata.objects.filter(token=token).filter(user__is_active=False).get()
            
            # Invalidar el token en UsersMetadata para evitar reutilización
            UsersMetadata.objects.filter(token=token).update(token="")
            
            # Actualizar el usuario: activa la cuenta (is_active = True)
            User.objects.filter(id=data.user_id).update(is_active=True)
            
            # Obtener la URL del frontend desde la variable de entorno
            frontend_url = os.getenv("BASE_URL_FRONTEND")
            
            # Reemplazar el marcador {user_id} por el ID real del usuario
            if frontend_url:
                frontend_url = frontend_url.replace("{user_id}", str(data.user_id))
            else:
                # Ruta por defecto en caso de que la variable de entorno no esté definida
                frontend_url = "/"
            
            # Redirigir al usuario al front-end para completar su perfil
            return HttpResponseRedirect(frontend_url)
        
        except UsersMetadata.DoesNotExist:
            # Si no se encuentra el token, lanzar un error 404
            raise Http404
        


class Login(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        password = request.data.get("password")

        # Verifica si los campos están presentes y no vacíos
        if not correo:
            return JsonResponse(
                {"estado": "error", "mensaje": "El campo 'correo' es obligatorio"},
                status=HTTPStatus.BAD_REQUEST,
            )
        if not password:
            return JsonResponse(
                {"estado": "error", "mensaje": "El campo 'password' es obligatorio"},
                status=HTTPStatus.BAD_REQUEST,
            )

        # Buscar usuario en la base de datos por correo
        try:
            user = User.objects.get(email=correo)
        except User.DoesNotExist:
            return JsonResponse(
                {"estado": "error", "mensaje": "El usuario no existe"},
                status=HTTPStatus.BAD_REQUEST,
            )

        # Autenticar usuario usando el username (no el correo)
        auth = authenticate(request, username=user.username, password=password)

        if auth is not None:  # Si la autenticación es correcta
            # Generamos una fecha de expiración (1 día después)
            fecha_expiracion = datetime.now() + timedelta(days=1)
            fecha_timestamp = int(fecha_expiracion.timestamp())

            # Generamos el payload del token
            payload = {
                "id": user.id,
                "iss": os.getenv("BASE_URL", "http://localhost:8000/"),  # URL base del sistema
                "iat": int(time.time()),  # Timestamp de creación
                "exp": fecha_timestamp,  # Expiración en UNIX timestamp
            }

            try:
                jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS512")
                return JsonResponse(
                    {
                        "id": user.id,
                        "nombre": user.first_name,
                        "token": jwt_token,
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {"estado": "error", "mensaje": f"Ocurrió un error inesperado: {str(e)}"},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

        # Si las credenciales son incorrectas
        return JsonResponse(
            {"estado": "error", "mensaje": "Las credenciales ingresadas no son correctas"},
            status=HTTPStatus.UNAUTHORIZED,
        )
        
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from datetime import datetime, timedelta
from .models import TokenRegistroTerapeuta
from .permissions import EsAdministrador

class GenerarTokenTerapeuta(APIView):
    permission_classes = [EsAdministrador]  # Solo administradores pueden generar tokens

    def get(self, request):
        # Genera un token único
        token = str(uuid.uuid4())
        # Define una fecha de expiración (por ejemplo, 24 horas)
        fecha_expiracion = datetime.now() + timedelta(hours=24)
        # Guarda el token en la base de datos
        TokenRegistroTerapeuta.objects.create(token=token, expiracion=fecha_expiracion)
        return Response({"token": token}, status=status.HTTP_200_OK)

class RegistroTerapeuta(APIView):
    permission_classes = [EsAdministrador]  # Solo administradores pueden registrar terapeutas

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"estado": "error", "mensaje": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verifica que el token sea válido y no haya expirado
        try:
            token_obj = TokenRegistroTerapeuta.objects.get(token=token, expiracion__gte=datetime.now())
        except TokenRegistroTerapeuta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "Token inválido o expirado"}, status=status.HTTP_403_FORBIDDEN)
        
        # Registra al terapeuta
        try:
            usuario = User.objects.create_user(
                username=request.data["nombre"],
                email=request.data["correo"],
                password=request.data["password"],
            )
            UserProfile.objects.create(user=usuario, rol='terapeuta')
            # Invalida el token después de su uso
            token_obj.delete()
            return Response({"estado": "éxito", "mensaje": "Terapeuta registrado correctamente"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)





#Actualización: Crea las vistas para generar tokens y registrar terapeutas.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from datetime import datetime, timedelta
from .models import TokenRegistroTerapeuta
from .permissions import EsAdministrador

class GenerarTokenTerapeuta(APIView):
    permission_classes = [EsAdministrador]  # Solo administradores pueden generar tokens

    def get(self, request):
        # Genera un token único
        token = str(uuid.uuid4())
        # Define una fecha de expiración (por ejemplo, 24 horas)
        fecha_expiracion = datetime.now() + timedelta(hours=24)
        # Guarda el token en la base de datos
        TokenRegistroTerapeuta.objects.create(token=token, expiracion=fecha_expiracion)
        return Response({"token": token}, status=status.HTTP_200_OK)

class RegistroTerapeuta(APIView):
    permission_classes = [EsAdministrador]  # Solo administradores pueden registrar terapeutas

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"estado": "error", "mensaje": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verifica que el token sea válido y no haya expirado
        try:
            token_obj = TokenRegistroTerapeuta.objects.get(token=token, expiracion__gte=datetime.now())
        except TokenRegistroTerapeuta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "Token inválido o expirado"}, status=status.HTTP_403_FORBIDDEN)
        
        # Registra al terapeuta
        try:
            usuario = User.objects.create_user(
                username=request.data["nombre"],
                email=request.data["correo"],
                password=request.data["password"],
            )
            UserProfile.objects.create(user=usuario, rol='terapeuta')
            # Invalida el token después de su uso
            token_obj.delete()
            return Response({"estado": "éxito", "mensaje": "Terapeuta registrado correctamente"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"estado": "error", "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)