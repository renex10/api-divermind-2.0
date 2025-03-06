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
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, time, timedelta
from jose import jwt  # o import jwt si usas PyJWT

class Login(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        password = request.data.get("password")

        # Verifica si los campos están presentes y no vacíos
        if not correo:
            return JsonResponse({"estado": "error", "mensaje": "El campo 'correo' es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not password:
            return JsonResponse({"estado": "error", "mensaje": "El campo 'password' es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        # Buscar usuario en la base de datos
        try:
            user = User.objects.get(email=correo)
            if not user.is_active:
                return JsonResponse({"estado": "error", "mensaje": "El usuario no está activo"}, status=HTTPStatus.BAD_REQUEST)
        except User.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El usuario no existe"}, status=HTTPStatus.BAD_REQUEST)

        # Autenticar usuario
        auth = authenticate(request, username=correo, password=password)  # Usa el correo como username

        if auth is not None:  # Si la autenticación es correcta
            # Generamos una fecha de expiración (1 día después)
            fecha_expiracion = datetime.now() + timedelta(days=1)
            fecha_timestamp = int(fecha_expiracion.timestamp())

            # Generamos el payload del token
            payload = {
                "id": user.id,
                "iss": os.getenv("BASE_URL", "http://localhost:8000/"),  # URL base del sistema
                "iat": int(time.time()),  # Timestamp de creación
                "exp": fecha_timestamp  # Expiración en UNIX timestamp
            }

            try:
                jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS512")
                return JsonResponse({"id": user.id, "nombre": user.first_name, "token": jwt_token})
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": f"Ocurrió un error inesperado: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        # Si las credenciales son incorrectas
        return JsonResponse({"estado": "error", "mensaje": "Las credenciales ingresadas no son correctas"}, status=HTTPStatus.UNAUTHORIZED)