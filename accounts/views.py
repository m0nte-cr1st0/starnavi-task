from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import (
    RegistrationSerializer,
    UserActivitySerializer,
    UserSerializer,
)


class RegistrationAPIView(generics.CreateAPIView):
    """Registration"""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """User create"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            data={
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User created successfully. Now perform Login to get your token",
            },
            status=status.HTTP_201_CREATED,
        )


class UserActivityAPIView(generics.RetrieveAPIView):
    """User activities"""

    permission_classes = (AllowAny,)
    serializer_class = UserActivitySerializer
    queryset = User.objects.all()
