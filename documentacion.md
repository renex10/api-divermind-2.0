el usaurio root en workbench 
root
clave divermind

usuario apidivermind
contraseña apidivermind
puerto 3306ss


## documentacion

entorno virtula activar

### ACTIVAR ENTORNO 
> .\entorno\Scripts\Activate.ps1

recuerda con etorno activado
creando proyecto:
1 instala django:
 > pip install Django
## INICIA SEL SERVIDOR:
> python manage.py runserver
s
2 django-admin startproject apidivermind

## instalando mysql

## conexion base de datos
base de datos = api 
root = api 
puerto 3306
contrseña =api 


creacion de migraciones
> python manage.py makemigrations
> python manage.py migrate

seguridad
usuario:apidivermind
correo:apidivermind@apidivermind.com
conntraseña:apidivermind
> python manage.py createsuperuser.
quiero saber si se guardo en la base de datos
```sql

SELECT * FROM auth_user WHERE is_superuser = 1;

```

extender la tabla auth_user

quiero saber los registro si funciona
POST: http://127.0.0.1:8000/api/v1/registro/


generando token

|                              |     |                    |       |                 |     |                                                                                               |                  |
| enviar la url en el correo   |---->|  click en el correo|-----> | abre un endpoint|---->| pregunta si existe este token si es un usuario que NO esta activo, BORRA EL TOKEN Y LOA aCTIVA |
|                              |     |                    |       |                 |     |                                                                                               | 


probando en postma body -> row
 username=request.data["nombre"],  # Nombre de usuario
                email=request.data["correo"],  # Correo electrónico
                password=request.data["password"],  # Contraseña
				
				
{
    "nombre": "Juan Pérez",
    "correo": "juan.perez@example.com",
    "password": "password123"
}

#### ENVIO DE CORREO DE VERIFICACION



###JWT IMPLEMENTACION
1 ###importando
> pip install python-jose[cryptography]
Primero debemos importar:

en archivo view.py:
from jose import jwt
from django.conf import setting
from datetime import datetime. timedelta

2- clave de contraseña para desifrar la contraseña: SETTING-> SECRET_KEY

### construir el token 
 
 
 
# creando decoradores

1 creando archivo llamado decorators.py
2 crear metodo:
```python
def logueado(redirect_url= None):
 def metodo(func):
     @wraps(func)
	 def _decorator(request, *args, **kwargs):
	    req = arg [0]
		if not req.header.get( 'Autorization) or req.headers.get('Autorization') = None:
		 json response(["estado":"error", "mensaje":"sin autorizacion},statud= httpsstarus.unautorized)
		header=reque.header.get("authorizarion:split("")
		try:
		  resuelto="jwt.decode(header=[1],setting.secret_key,añgothimo=´'hs5122])"
		 except Exeption as e:
		 return jsonresponse (sin autiorizacicion
		 status no autoizado
     return _decorator
return metodo
 ```
 
 
python manage.py makemigrations
python manage.py migrate



###flujo y preguntas claves del sistema
Resumen del Flujo

    Registro del Terapeuta:

        El terapeuta se registra en el sistema con un rol específico.

        Una vez registrado, el terapeuta puede registrar niños y asociar a sus familias.

    Registro del Niño y la Familia:

        El terapeuta registra a un niño en el sistema.

        Asocia a los padres (familia) del niño.

    Registro del Profesor:

        El profesor se registra en el sistema con un rol de "educador".

    Solicitud de Vinculación:

        El profesor envía una solicitud de acceso para vincularse a un niño específico.

    Notificación al Terapeuta:

        El sistema notifica al terapeuta sobre la solicitud de vinculación.

    Aprobación del Terapeuta:

        El terapeuta aprueba o rechaza la solicitud de vinculación.

    Notificación a los Padres:

        Si el terapeuta aprueba la solicitud, el sistema notifica a los padres para que den su consentimiento.

    Consentimiento de los Padres:

        Los padres aprueban o rechazan la solicitud.

    Acceso del Profesor:

        Si los padres dan su consentimiento, el profesor obtiene acceso restringido a la información del niño.

Elementos Clave del Sistema
Actores

    Terapeuta:

        Se registra en el sistema.

        Registra niños y asocia a sus familias.

        Aprueba o rechaza solicitudes de vinculación de profesores.

    Profesor:

        Se registra en el sistema.

        Envía solicitudes de vinculación para acceder a la información de un niño.

    Padre:

        Recibe notificaciones sobre solicitudes de vinculación.

        Da su consentimiento (o lo rechaza) para que el profesor acceda a la información del niño.

Entidades (Tablas Clave)

    Usuario:

        Almacena información de todos los usuarios (terapeutas, profesores, padres).

        Incluye campos como id, nombre, correo, rol, etc.

    Terapeuta:

        Extiende la tabla Usuario para agregar información específica del terapeuta.

    Nino:

        Almacena información de los niños registrados.

        Campos: id, nombre, fecha_nacimiento, terapeuta_id, familia_id.

    Familia:

        Almacena información de las familias (padres) asociadas a un niño.

        Campos: id, nombre, correo, telefono, etc.

    Profesor:

        Extiende la tabla Usuario para agregar información específica del profesor.

    Solicitud_Vinculacion_Profesor:

        Almacena las solicitudes de vinculación enviadas por los profesores.

        Campos: id, profesor_id, nino_id, estado (pendiente, aprobada, rechazada).

    Autorizacion_Profesor:

        Almacena las autorizaciones concedidas a los profesores.

        Campos: id, solicitud_id, padre_id, fecha_aprobacion.

    Notificaciones:

        Almacena las notificaciones enviadas a los usuarios.

        Campos: id, usuario_id, mensaje, fecha, leida.

    Acceso_Compartido:

        Almacena los accesos concedidos a los profesores.

        Campos: id, profesor_id, nino_id, fecha_acceso.

Flujo Detallado
1. Registro del Terapeuta

    El terapeuta se registra en el sistema.

    Se le asigna el rol de "terapeuta".

    Una vez registrado, puede iniciar sesión y acceder a las funcionalidades del sistema.

2. Registro del Niño y la Familia

    El terapeuta registra a un niño en el sistema.

    Asocia a los padres (familia) del niño.

    La información del niño y la familia se almacena en las tablas Nino y Familia.

3. Registro del Profesor

    El profesor se registra en el sistema.

    Se le asigna el rol de "educador".

    Una vez registrado, puede enviar solicitudes de vinculación.

4. Solicitud de Vinculación

    El profesor selecciona un niño y envía una solicitud de vinculación.

    La solicitud se almacena en la tabla Solicitud_Vinculacion_Profesor.

5. Notificación al Terapeuta

    El sistema notifica al terapeuta sobre la solicitud de vinculación.

    La notificación se almacena en la tabla Notificaciones.

6. Aprobación del Terapeuta

    El terapeuta revisa la solicitud y decide aprobarla o rechazarla.

    Si la aprueba, el sistema notifica a los padres.

    Si la rechaza, el sistema notifica al profesor y finaliza el proceso.

7. Notificación a los Padres

    Si el terapeuta aprueba la solicitud, el sistema notifica a los padres.

    La notificación se almacena en la tabla Notificaciones.

8. Consentimiento de los Padres

    Los padres revisan la solicitud y deciden dar su consentimiento o rechazarla.

    Si dan su consentimiento, el sistema concede acceso al profesor.

    Si lo rechazan, el sistema notifica al profesor y finaliza el proceso.

9. Acceso del Profesor

    Si los padres dan su consentimiento, el profesor obtiene acceso restringido a la información del niño.

    El acceso se registra en la tabla Acceso_Compartido.

Diagrama de Casos de Uso
plaintext
Copy

+-------------------+
|    Sistema        |
+-------------------+
|                   |
| 1. Registrar Niño |
| 2. Registrar Familia |
| 3. Enviar Solicitud |
| 4. Aprobar Solicitud |
| 5. Dar Consentimiento |
| 6. Conceder Acceso |
+-------------------+
        ^  ^  ^
        |  |  |
        |  |  +-------------------+
        |  |                      |
        |  +-------------------+  |
        |                      |  |
+-------+-------+      +-------+-------+      +-------+
|  Terapeuta    |      |  Profesor     |      |  Padre |
+---------------+      +---------------+      +-------+

Conclusión

Este flujo describe un sistema bien estructurado en el que los terapeutas, profesores y padres interactúan para gestionar el acceso a la información de los niños. Las tablas clave y los casos de uso están claramente definidos, lo que facilita la implementación del sistema.




Preguntas Clave
1. Sobre los Roles y Permisos

    ¿Cómo se asignan los roles (terapeuta, profesor, padre) a los usuarios?

    ¿Qué permisos tiene cada rol? Por ejemplo:

        ¿Puede un terapeuta ver la información de todos los niños, o solo de los que ha registrado?

        ¿Puede un profesor ver la información de todos los niños, o solo de aquellos a los que ha sido vinculado?

        ¿Pueden los padres ver la información de otros niños o solo la de su hijo?

    ¿Cómo se manejan los casos en los que un usuario tiene múltiples roles (por ejemplo, un padre que también es profesor)?

2. Sobre el Registro de Niños y Padres

    ¿Cómo se asocia un niño a un terapeuta específico? ¿Se hace automáticamente al registrarlo, o se puede asignar manualmente?

    ¿Qué sucede si un niño tiene más de dos padres o tutores? ¿Cómo se maneja esta situación en el sistema?

    ¿Se puede transferir un niño de un terapeuta a otro? Si es así, ¿cómo se maneja esta transferencia?

3. Sobre las Solicitudes de Vinculación

    ¿Qué información se incluye en una solicitud de vinculación? Por ejemplo:

        ¿Se incluye el nombre del niño, el nombre del profesor y el motivo de la solicitud?

    ¿Qué sucede si un profesor envía una solicitud de vinculación a un niño que ya tiene acceso? ¿Se rechaza automáticamente o se notifica al terapeuta?

    ¿Cómo se manejan las solicitudes de vinculación rechazadas? ¿Se permite al profesor volver a enviar una solicitud para el mismo niño?

4. Sobre las Notificaciones

    ¿Cómo se envían las notificaciones a los usuarios? Por ejemplo:

        ¿Se envían por correo electrónico, mensajes dentro del sistema, o ambos?

    ¿Qué sucede si un usuario no revisa una notificación? ¿Se le envía un recordatorio?

    ¿Cómo se manejan las notificaciones para usuarios que no tienen acceso frecuente al sistema (por ejemplo, padres que no revisan el sistema regularmente)?

5. Sobre el Acceso a la Información

    ¿Qué información específica puede ver un profesor una vez que se le concede acceso a un niño? Por ejemplo:

        ¿Puede ver toda la información del niño, o solo ciertos datos (como nombre, edad, etc.)?

    ¿Cómo se maneja la confidencialidad de la información? Por ejemplo:

        ¿Se cifran los datos sensibles en la base de datos?

        ¿Se registran los accesos a la información para auditar quién ha visto qué?

6. Sobre la Lista de Niños

    ¿Cómo se genera la lista de niños según el rol del usuario? Por ejemplo:

        Si un terapeuta inicia sesión, ¿ve solo los niños que ha registrado?

        Si un profesor inicia sesión, ¿ve solo los niños a los que ha sido vinculado?

        Si un padre inicia sesión, ¿ve solo la información de su hijo?

    ¿Se pueden filtrar y ordenar las listas de niños? Por ejemplo:

        ¿Se puede filtrar por nombre, edad, fecha de registro, etc.?

7. Sobre la Asignación de IDs

    ¿Cómo se asignan los IDs a los niños y padres? Por ejemplo:

        ¿Se generan automáticamente al registrarlos?

        ¿Se pueden editar o cambiar después de la asignación?

    ¿Qué sucede si un niño o padre tiene un ID duplicado? ¿Cómo se maneja esta situación?

Supuestos
1. Sobre los Roles

    Suponemos que cada usuario tiene un solo rol (terapeuta, profesor o padre). Si un usuario necesita tener múltiples roles, se debe definir cómo se manejará esto.

    Suponemos que los permisos de cada rol están claramente definidos y no cambian con el tiempo.

2. Sobre el Registro de Niños y Padres

    Suponemos que cada niño está asociado a un solo terapeuta y a una sola familia (padres).

    Suponemos que los padres no pueden registrar niños directamente; solo los terapeutas pueden hacerlo.

3. Sobre las Solicitudes de Vinculación

    Suponemos que un profesor solo puede enviar una solicitud de vinculación a un niño a la vez.

    Suponemos que el terapeuta y los padres deben aprobar la solicitud para que el profesor obtenga acceso.

4. Sobre las Notificaciones

    Suponemos que las notificaciones se envían automáticamente cuando ocurre un evento importante (por ejemplo, una nueva solicitud de vinculación).

    Suponemos que los usuarios pueden marcar las notificaciones como "leídas" para gestionarlas mejor.

5. Sobre el Acceso a la Información

    Suponemos que los profesores solo tienen acceso a la información necesaria para su trabajo (por ejemplo, no pueden ver datos médicos confidenciales).

    Suponemos que los padres solo pueden ver la información de su hijo y no tienen acceso a la información de otros niños.

6. Sobre la Lista de Niños

    Suponemos que la lista de niños se genera dinámicamente según el rol del usuario que inicia sesión.

    Suponemos que los filtros y ordenamientos son opcionales y no afectan la funcionalidad básica del sistema.

7. Sobre la Asignación de IDs

    Suponemos que los IDs se generan automáticamente y no pueden ser editados por los usuarios.

    Suponemos que no habrá IDs duplicados debido a la implementación de restricciones en la base de datos.

Preguntas Adicionales

    ¿Cómo se manejan los errores en el sistema?

        Por ejemplo, ¿qué sucede si un profesor intenta enviar una solicitud de vinculación a un niño que no existe?

        ¿Cómo se notifica al usuario sobre errores (por ejemplo, campos obligatorios faltantes)?

    ¿Cómo se maneja la seguridad de los datos?

        ¿Se utiliza HTTPS para proteger las comunicaciones entre el cliente y el servidor?

        ¿Se almacenan las contraseñas de los usuarios de forma segura (por ejemplo, usando hash)?

    ¿Cómo se manejan las actualizaciones de información?

        ¿Puede un terapeuta editar la información de un niño después de registrarlo?

        ¿Qué sucede si un padre cambia su información de contacto? ¿Se notifica automáticamente al terapeuta?

    ¿Cómo se manejan los casos de eliminación de datos?

        ¿Qué sucede si un terapeuta elimina a un niño del sistema? ¿Se elimina también la información asociada (por ejemplo, solicitudes de vinculación)?

        ¿Qué sucede si un padre solicita que se elimine su información del sistema?


Preguntas Clave Adicionales
1. Sobre la Escalabilidad

    ¿Cómo se manejará el sistema si el número de usuarios (terapeutas, profesores, padres) crece significativamente?

    ¿El sistema está diseñado para soportar múltiples instituciones (por ejemplo, varias escuelas o clínicas) o solo una?

    ¿Cómo se manejará la carga de trabajo si hay un aumento en el número de solicitudes de vinculación o notificaciones?

2. Sobre la Usabilidad

    ¿Cómo se garantiza que la interfaz de usuario sea intuitiva y fácil de usar para todos los roles (terapeutas, profesores, padres)?

    ¿Se proporcionará capacitación o documentación para los usuarios que no estén familiarizados con el sistema?

    ¿Cómo se manejarán los casos en los que un usuario olvida su contraseña o tiene problemas para iniciar sesión?

3. Sobre la Integración con Otros Sistemas

    ¿El sistema necesita integrarse con otras plataformas o herramientas (por ejemplo, sistemas de gestión escolar, historiales médicos electrónicos)?

    ¿Cómo se manejará la sincronización de datos entre este sistema y otros sistemas externos?

    ¿Se proporcionará una API para que otros sistemas puedan interactuar con este sistema?

4. Sobre la Privacidad y Cumplimiento Normativo

    ¿Cómo se garantiza que el sistema cumpla con las regulaciones de privacidad de datos (por ejemplo, GDPR, HIPAA)?

    ¿Se obtendrá el consentimiento explícito de los padres antes de compartir la información de sus hijos con los profesores?

    ¿Cómo se manejarán las solicitudes de eliminación de datos (derecho al olvido) según las regulaciones aplicables?

5. Sobre la Gestión de Errores y Excepciones

    ¿Cómo se manejarán los errores inesperados (por ejemplo, fallos en la base de datos, errores de red)?

    ¿Se proporcionará un registro de errores (logging) para facilitar la depuración y el mantenimiento?

    ¿Cómo se notificará a los usuarios sobre errores y cómo se les guiará para resolverlos?

6. Sobre la Personalización y Configuración

    ¿Se permitirá a los terapeutas personalizar ciertos aspectos del sistema (por ejemplo, campos adicionales para los registros de niños)?

    ¿Se podrán configurar reglas específicas para las notificaciones (por ejemplo, notificar solo en ciertos horarios)?

    ¿Se permitirá a los usuarios cambiar su información de perfil (por ejemplo, correo electrónico, número de teléfono)?

Problemas Potenciales
1. Problemas de Rendimiento

    Carga de la Base de Datos: Si el número de niños, padres y profesores crece rápidamente, la base de datos podría volverse lenta.

        Solución: Implementar índices en la base de datos y optimizar las consultas.

    Notificaciones Masivas: Si hay muchas notificaciones que enviar, el sistema podría ralentizarse.

        Solución: Usar colas de mensajes (por ejemplo, RabbitMQ, Kafka) para manejar notificaciones de manera asíncrona.

2. Problemas de Seguridad

    Ataques de Fuerza Bruta: Los atacantes podrían intentar adivinar contraseñas de usuarios.

        Solución: Implementar límites de intentos de inicio de sesión y usar autenticación de dos factores (2FA).

    Exposición de Datos Sensibles: Si no se cifran los datos sensibles, podrían ser accesibles en caso de una brecha de seguridad.

        Solución: Cifrar datos sensibles en la base de datos y usar HTTPS para las comunicaciones.

3. Problemas de Usabilidad

    Interfaz Confusa: Si la interfaz de usuario no es intuitiva, los usuarios podrían tener dificultades para usar el sistema.

        Solución: Realizar pruebas de usabilidad con usuarios reales y ajustar el diseño según sus comentarios.

    Falta de Retroalimentación: Si los usuarios no reciben retroalimentación clara sobre sus acciones (por ejemplo, al enviar una solicitud), podrían sentirse frustrados.

        Solución: Mostrar mensajes claros y concisos después de cada acción importante.

4. Problemas de Mantenimiento

    Falta de Documentación: Si el sistema no está bien documentado, será difícil para nuevos desarrolladores entender y mantener el código.

        Solución: Documentar el código, las APIs y los procesos clave.

    Actualizaciones Problemáticas: Si no se gestionan correctamente las actualizaciones del sistema, podrían introducir errores.

        Solución: Implementar pruebas automatizadas y un proceso de despliegue continuo (CI/CD).

Sugerencias
1. Mejoras en la Interfaz de Usuario

    Panel de Control Personalizado: Crear un panel de control personalizado para cada rol (terapeuta, profesor, padre) que muestre solo la información relevante.

    Búsqueda y Filtrado Avanzado: Permitir a los usuarios buscar y filtrar niños, solicitudes y notificaciones de manera avanzada (por ejemplo, por fecha, estado, etc.).

2. Mejoras en la Seguridad

    Autenticación de Dos Factores (2FA): Implementar 2FA para agregar una capa adicional de seguridad.

    Auditoría de Accesos: Registrar todos los accesos a la información sensible para poder auditar quién ha visto qué y cuándo.

3. Mejoras en la Escalabilidad

    Caché: Usar caché (por ejemplo, Redis) para almacenar datos frecuentemente accedidos y reducir la carga en la base de datos.

    Balanceo de Carga: Implementar balanceo de carga si el sistema necesita manejar un gran número de usuarios simultáneamente.

4. Mejoras en la Gestión de Notificaciones

    Notificaciones Personalizadas: Permitir a los usuarios personalizar cómo y cuándo reciben notificaciones (por ejemplo, por correo electrónico, mensajes en la aplicación, etc.).

    Recordatorios Automáticos: Enviar recordatorios automáticos si una solicitud de vinculación no ha sido revisada en un cierto período de tiempo.

5. Mejoras en la Integración

    API Pública: Proporcionar una API pública para que otros sistemas puedan interactuar con este sistema (por ejemplo, para sincronizar datos con sistemas escolares).

    Webhooks: Implementar webhooks para notificar a otros sistemas sobre eventos importantes (por ejemplo, cuando se aprueba una solicitud de vinculación).


    