from functools import wraps
from django.http import JsonResponse
from http import HTTPStatus
from jose import jwt
from django.conf import settings
import time
from django.contrib.auth.models import User
from registros.models import UserProfile

def logueado(rol_requerido=None):
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            # Verifica el token JWT
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse({"estado": "error", "mensaje": "No autorizado"}, status=HTTPStatus.UNAUTHORIZED)

            try:
                token = auth_header.split(" ")[1]  # Extrae el token del encabezado
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS512'])
                
                # Verifica la expiración del token
                if int(payload["exp"]) < int(time.time()):
                    return JsonResponse({"estado": "error", "mensaje": "Token expirado"}, status=HTTPStatus.UNAUTHORIZED)

                # Obtiene el usuario desde el token
                user_id = payload.get("id")
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)

                # Verifica el rol del usuario (si se especifica un rol requerido)
                if rol_requerido and user_profile.rol != rol_requerido:
                    return JsonResponse({"estado": "error", "mensaje": "No tienes permiso para realizar esta acción"}, status=HTTPStatus.FORBIDDEN)

                # Asigna el usuario autenticado a request.user
                request.user = user

            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "No autorizado"}, status=HTTPStatus.UNAUTHORIZED)

            # Si todo está bien, ejecuta la vista
            return func(request, *args, **kwargs)
        return _decorator
    return metodo