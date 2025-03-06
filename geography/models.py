from django.db import models

class Pais(models.Model):
    """
    Modelo que representa un país.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre del país")
    codigo_iso = models.CharField(max_length=2, blank=True, null=True, verbose_name="Código ISO")
    prefijo_telefono = models.CharField(max_length=10, blank=True, null=True, verbose_name="Prefijo telefónico")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Region(models.Model):
    """
    Modelo que representa una región asociada a un país.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la región")
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, verbose_name="País")

    def __str__(self):
        return f"{self.nombre} ({self.id_pais.nombre})"

    class Meta:
        db_table = 'Region'
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


class Comuna(models.Model):
    """
    Modelo que representa una comuna asociada a una región.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la comuna")
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Región")

    def __str__(self):
        return f"{self.nombre} ({self.id_region.nombre})"

    class Meta:
        db_table = 'Comuna'
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'


class Direccion(models.Model):
    """
    Modelo que representa una dirección, asociada a una comuna.
    """
    TIPO_VIVIENDA_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('oficina', 'Oficina'),
        ('otro', 'Otro')
    ]

    calle = models.CharField(max_length=255, verbose_name="Calle")
    numero = models.CharField(max_length=20, verbose_name="Número")
    tipo_vivienda = models.CharField(
        max_length=20,
        choices=TIPO_VIVIENDA_CHOICES,
        default='casa',
        verbose_name="Tipo de vivienda"
    )
    bloque = models.CharField(max_length=20, blank=True, null=True, verbose_name="Bloque")
    departamento = models.CharField(max_length=20, blank=True, null=True, verbose_name="Departamento")
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name="Comuna")

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.id_comuna.nombre}"

    class Meta:
        db_table = 'Direccion'
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'