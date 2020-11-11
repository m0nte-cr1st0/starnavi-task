from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer


class PostCreateAPIView(generics.CreateAPIView):
    """Creat post"""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Pass user from request"""
        serializer.save(author=self.request.user)
