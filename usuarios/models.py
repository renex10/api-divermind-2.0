# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from geography.models import Pais, Direccion  # Asegúrate de que estos modelos existen

class Usuario(AbstractUser):
    ROLES = (
        ('terapeuta', 'Terapeuta'),
        ('educador', 'Educador'),
        ('familia', 'Familia'),
        ('escuela', 'Escuela'),
        ('centro_rehabilitacion', 'Centro de Rehabilitación')
    )
    
    # Campos personalizados
    rut = models.CharField(max_length=12, unique=True)
    rol = models.CharField(max_length=21, choices=ROLES)
    estado = models.CharField(max_length=8, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    id_pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)
    id_direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True, blank=True)
    imagen_perfil = models.ForeignKey('archivos.Imagen', on_delete=models.SET_NULL, null=True, blank=True)  # Usa una referencia de cadena

    # Campos heredados de AbstractUser (para resolver conflictos)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="usuarios_usuario_groups",  # ¡Custom related_name!
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuarios_usuario_permissions",  # ¡Custom related_name!
        related_query_name="usuario",
    )

    class Meta:
        db_table = 'auth_user'  # Opcional: Mantén la misma tabla si ya tienes datos