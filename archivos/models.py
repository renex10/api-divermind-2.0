# archivos/models.py
from django.db import models

class Imagen(models.Model):
    TIPOS_IMAGEN = (
        ('logo', 'Logo'),
        ('perfil', 'Perfil'),
        ('documento', 'Documento'),
        ('otro', 'Otro')
    )
    
    archivo = models.ImageField(upload_to='imagenes/')
    tipo = models.CharField(max_length=20, choices=TIPOS_IMAGEN)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    propietario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)  # Usa una referencia de cadena

    def __str__(self):
        return f"{self.tipo} - {self.archivo.name}"
