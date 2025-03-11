# Registro del Niño

URL de la API:  
[http://127.0.0.1:8000/api/v1/registros/registro-nino/](http://127.0.0.1:8000/api/v1/registros/registro-nino/)

El terapeuta registra en la base de datos con la siguiente estructura JSON:

```json
{
    "nombre": "carmencho",
    "fecha_nacimiento": "2020-01-01",
    "terapeuta": 32,
    "padres": [34]
}
```
resultados:
```json
{
    "id": 5,
    "nombre": "carmencho",
    "fecha_nacimiento": "2020-01-01",
    "terapeuta": 32,
    "padres": [
        34
    ]
}
```


---
---
---

http://127.0.0.1:8000/api/v1/registros/registro-terapeuta/

registro del terapeuta no olvides que le llega un correo para que el estado cambio 1:

```json
{
    "nombre": "richard",
    "correo": "richard@terapeuta.com",
    "password": "password123"
}
```

resultados:
```json
{
    "estado": "éxito",
    "mensaje": "Terapeuta registrado correctamente",
    "perfil": {
        "id": 9,
        "user": 32,
        "rol": "terapeuta"
    }
}
```
---
---
---
http://127.0.0.1:8000/api/v1/seguridad/login/
ingreso de usuario normal:
```json
{
"correo": "richard@terapeuta.com",
"password": "password123"
}
```

resultados:
```json
{
    "id": 32,
    "nombre": "",
    "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzIsImlzcyI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC8iLCJpYXQiOjE3NDE0MzExMjgsImV4cCI6MTc0MTUxNzUyOH0.AkT5NfPZsZ0_zuumP7gL2l_5sOCe8oYBizH0EJJ_46vZ0w3_e7k-86udLERdMN4hK1O9a7HBA7YHaS4zsuOaOw"
}
```
---
---
---
http://127.0.0.1:8000/api/v1/registros/registro-profesor/

registrar a un profesor:

```json
{
    "nombre": "ProfesorEjemplo",
    "correo": "profesor@example.com",
    "password": "contraseña_segura"
}
```

resultados:
```json

{
    "estado": "éxito",
    "mensaje": "Profesor registrado correctamente",
    "perfil": {
        "id": 10,
        "user": 33,
        "rol": "profesor"
    }
}
```

registro de un padre en el sistema:
http://127.0.0.1:8000/api/v1/registros/registro-padre/

```json
{
{
    "nombre": "PadreEjemplo",
    "correo": "padre@example.com",
    "password": "contraseña_segura"
}
}
```

resultado al registrar a un padre:
```json
{
{
   {
    "estado": "éxito",
    "mensaje": "Padre registrado correctamente",
    "perfil": {
        "id": 11,
        "user": 34,
        "rol": "padre"
    }
}
}
}
```


## El profesor envía una solicitud de vinculación:

    El profesor autenticado envía una solicitud POST a la URL http://127.0.0.1:8000/api/v1/registros/solicitud-vinculacion/.

    El cuerpo de la solicitud debe incluir el ID del niño (nino_id).

    1. ingreso con las credenciales del profesor(no olvides que debes tener el token y estar en estado 1):
```json
    {


   "correo": "profesor@example.com",
    "password": "contraseña_segura"
    }
```
    2. lo cual me permite dentro de  http://127.0.0.1:8000/api/v1/registros/solicitud-vinculacion/
 pasarle el ID del niño:

 ```json
    {
{
    "nino_id": 1  // ID del niño al que se solicita acceso
}
    }


----
----
----

### tareas a realizar:
    Notificación al Terapeuta:

        Implementar un sistema de notificaciones para informar al terapeuta cuando se envíe una solicitud de vinculación.

    Aprobación del Terapeuta:

        Crear una vista que permita al terapeuta aprobar o rechazar las solicitudes de vinculación.

    Notificación a los Padres:

        Implementar un sistema de notificaciones para informar a los padres cuando el terapeuta apruebe una solicitud.

    Consentimiento de los Padres:

        Crear una vista que permita a los padres dar su consentimiento o rechazar la solicitud.

    Acceso del Profesor:

        Implementar la lógica para conceder acceso al profesor una vez que los padres den su consentimiento.

> Content-Type | > application/json
> Authorization | > Bearer 


