from rest_framework import serializers
from .models import UserProfile
from .models import Nino


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserProfile.
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'rol']
        read_only_fields = ['id', 'user']  # El ID y el usuario no se pueden modificar directamente
        
 #Serializer para el Niño

#Necesitamos un serializer para validar y procesar los datos del niño.
#Archivo registros/serializers.py

from rest_framework import serializers
from .models import Nino

class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'fecha_nacimiento', 'terapeuta']
        read_only_fields = ['id', 'terapeuta']  # El ID y el terapeuta no se pueden modificar directamente





class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'rol']
        read_only_fields = ['id', 'user']  # El ID y el usuario no se pueden modificar directamente

""" class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'fecha_nacimiento'] """