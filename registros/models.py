from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Modelo para extender el usuario con un rol.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLES = [
        ('terapeuta', 'Terapeuta'),
        ('profesor', 'Profesor'),
        ('padre', 'Padre'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
    
class Nino(models.Model):
    """
    Modelo para representar a un niño.
    """
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    terapeuta = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ninos_registrados')
    padres = models.ManyToManyField(User, related_name='hijos')  # Relación con usuarios (padres)

    def __str__(self):
        return self.nombre   
    
    

        
 #Este modelo se encargará de almacenar las solicitudes de vinculación en la base de datos.  
class SolicitudVinculacion(models.Model):
    # Opciones para el estado de la solicitud
    ESTADOS = [
        ('pendiente', 'Pendiente'),  # Estado inicial de la solicitud
        ('aprobada', 'Aprobada'),    # Solicitud aprobada por el terapeuta
        ('rechazada', 'Rechazada'),  # Solicitud rechazada por el terapeuta
    ]
    
    # Relación con el profesor que envía la solicitud
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_vinculacion')
    
    # Relación con el niño al que se solicita acceso
    nino = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='solicitudes_vinculacion')
    
    # Estado de la solicitud (por defecto es "pendiente")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    # Fecha en que se envió la solicitud (se asigna automáticamente)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Representación en cadena de la solicitud
        return f"Solicitud de {self.profesor.username} para {self.nino.nombre}"
    

class Notificacion(models.Model):
    # Usuario al que se dirige la notificación
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    
    # Mensaje de la notificación
    mensaje = models.CharField(max_length=255)
    
    # Fecha en que se creó la notificación
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Estado de la notificación (leída o no leída)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.mensaje}"