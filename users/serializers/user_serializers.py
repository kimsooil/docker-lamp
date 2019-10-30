from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
            'is_staff'
        ]
        read_only_fields = ['email', 'is_staff']