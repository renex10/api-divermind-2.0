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
    
    
    

#necesitamos un modelo para representar a los niños. Este modelo estará relacionado con el terapeuta que lo registra.

#class Nino(models.Model):
    """
    Modelo para representar a un niño.
    """
    #nombre = models.CharField(max_length=100)
    #fecha_nacimiento = models.DateField()
    #terapeuta = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ninos_registrados')

    #def __str__(self):
        #return self.nombre