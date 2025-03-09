from rest_framework import serializers
from django.contrib.auth.models import User  # Importar el modelo User
from .models import UserProfile, Nino  # Importar los modelos necesarios

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserProfile.
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'rol']
        read_only_fields = ['id', 'user']  # El ID y el usuario no se pueden modificar directamente

class NinoSerializer(serializers.ModelSerializer):
    # Campo para los padres (solo usuarios con rol "padre")
    padres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(profile__rol='padre'),  # Filtra solo usuarios con rol "padre"
        required=True
    )

    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'fecha_nacimiento', 'terapeuta', 'padres']

    def create(self, validated_data):
        # Extraer los IDs de los padres
        padres = validated_data.pop('padres')
        
        # Crear el niño
        nino = Nino.objects.create(**validated_data)
        
        # Asignar los padres al niño
        nino.padres.set(padres)
        
        return nino