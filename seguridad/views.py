from django.shortcuts import render
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
#from django.core.exceptions import Http404

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Clase Registro que maneja las solicitudes POST para el registro de usuarios
class Registro(APIView):
    def post(self, request):
        """
        Maneja las solicitudes POST para registrar un nuevo usuario.
        Verifica que los campos 'nombre', 'correo' y 'password' estén presentes y no estén vacíos.
        Devuelve una respuesta JSON con el estado y un mensaje correspondiente.
        """
        
        # Verifica si el campo 'nombre' está presente y no está vacío
        if request.data.get("nombre") is None or not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo 'nombre' es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        # Verifica si el campo 'correo' está presente y no está vacío
        if request.data.get("correo") is None or not request.data.get("correo"):
            return JsonResponse({"estado": "error", "mensaje": "El campo 'correo' es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        # Verifica si el campo 'password' está presente y no está vacío
        if request.data.get("password") is None or not request.data.get("password"):
            return JsonResponse({"estado": "error", "mensaje": "El campo 'password' es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            # Crea un nuevo usuario en la tabla de autenticación
            u = User.objects.create_user(
                username=request.data["nombre"],  # Nombre de usuario
                email=request.data["correo"],  # Correo electrónico
                password=request.data["password"],  # Contraseña
                is_active=False  # El usuario no está activo por defecto
            )
            
            # Genera un token único
            token = str(uuid.uuid4())
            
            # Crea una entrada en UsersMetadata con el token y el usuario
            UsersMetadata.objects.create(token=token, user=u)
            
            # Guarda el usuario
            u.save()
            
            # Genera la URL utilizando f-string correctamente
            url = f"{os.getenv('base_URL')}/api/v1/verificacion/{token}"
            
            # HTML con estilo neumorfismo
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
            
        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la creación del usuario
            return JsonResponse(
                {"estado": "error", "mensaje": "Ocurrió un error inesperado: " + str(e)},
                status=HTTPStatus.BAD_REQUEST
            )
        
        # Imprime la URL en la consola
        print(url)
        
        # Devuelve una respuesta de éxito con el token
        return JsonResponse({"estado": "éxito", "mensaje": "Registro exitoso", "token": token}, status=HTTPStatus.OK)

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