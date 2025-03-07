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