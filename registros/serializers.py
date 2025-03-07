from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserProfile.
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'rol']
        read_only_fields = ['id', 'user']  # El ID y el usuario no se pueden modificar directamente