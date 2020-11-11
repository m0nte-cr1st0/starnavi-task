from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer"""

    class Meta:
        """."""

        model = User
        fields = ("id", "username", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "max_length": 128,
                "min_length": 8,
            },
        }

    def create(self, validated_data):
        """Create user"""
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        """."""

        model = User
        fields = "__all__"


class UserActivitySerializer(serializers.ModelSerializer):
    """User activities serializer"""

    class Meta:
        """Last login and last request"""

        model = User
        fields = ("last_login", "last_request")
