from django.db import models  # Importa el módulo models de Django para definir los modelos de la base de datos
from django.contrib.auth.models import User  # Importa el modelo User del módulo de autenticación de Django

# Define el modelo UsersMetadata
class UsersMetadata(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)  # Relación de clave foránea con el modelo User
    token = models.CharField(max_length=100, blank=True, null=True)  # Campo de texto con longitud máxima de 100 caracteres, puede estar vacío o ser nulo
    
    # Define la representación en cadena del objeto
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  # Devuelve el nombre y apellido del usuario asociado
    
    # Define opciones de metadatos para el modelo
    class Meta:
        db_table = 'users_metadata'  # Cambia el nombre de la tabla a 'users_metadata'
        verbose_name = "User metadata"  # Nombre legible para humanos del modelo en singular
        verbose_name_plural = "User metadata"  # Nombre legible para humanos del modelo en plural
        
        
class TokenRegistroTerapeuta(models.Model):
    token = models.CharField(max_length=100, unique=True)
    expiracion = models.DateTimeField()

    def __str__(self):
        return f"Token: {self.token} (Expira: {self.expiracion})"