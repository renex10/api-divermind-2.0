from functools import wraps  # Importamos wraps para preservar los metadatos de la función decorada
from django.http import JsonResponse  # Para devolver respuestas JSON
from django.conf import settings  # Para acceder a la SECRET_KEY de Django
from jose import jwt  # Para decodificar el token JWT (usa python-jose)
from http import HTTPStatus  # Para usar códigos de estado HTTP

def logueado(redirect_url=None):
    """
    Decorador para verificar si el usuario está autenticado mediante un token JWT.
    Si el token no es válido o no está presente, devuelve un error 401 (No autorizado).

    Parámetros:
        redirect_url (str): URL a la que redirigir en caso de no estar autenticado (no implementado aquí).
    """
    def metodo(func):
        @wraps(func)  # Preserva los metadatos de la función original
        def _decorator(request, *args, **kwargs):
            """
            Función interna del decorador que verifica el token JWT.
            """
            # Verificamos si el encabezado 'Authorization' está presente en la solicitud
            if not request.headers.get('Authorization'):
                return JsonResponse(
                    {"estado": "error", "mensaje": "Sin autorización"},
                    status=HTTPStatus.UNAUTHORIZED
                )

            # Obtenemos el token del encabezado 'Authorization'
            header = request.headers.get('Authorization')
            try:
                # Separamos el token del prefijo 'Bearer' (si está presente)
                token = header.split(" ")[1]  # Formato esperado: "Bearer <token>"
            except IndexError:
                return JsonResponse(
                    {"estado": "error", "mensaje": "Formato de token inválido"},
                    status=HTTPStatus.UNAUTHORIZED
                )

            try:
                # Decodificamos el token usando la SECRET_KEY de Django
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
                # Si el token es válido, continuamos con la ejecución de la función original
                return func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                # Si el token ha expirado
                return JsonResponse(
                    {"estado": "error", "mensaje": "Token expirado"},
                    status=HTTPStatus.UNAUTHORIZED
                )
            except jwt.JWTError:
                # Si el token es inválido
                return JsonResponse(
                    {"estado": "error", "mensaje": "Token inválido"},
                    status=HTTPStatus.UNAUTHORIZED
                )
            except Exception as e:
                # Para cualquier otro error inesperado
                return JsonResponse(
                    {"estado": "error", "mensaje": f"Error inesperado: {str(e)}"},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

        return _decorator  # Devolvemos la función decorada
    return metodo  # Devolvemos el decorador