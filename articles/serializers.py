from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Post create serializer"""

    slug = serializers.SlugField(required=False)

    class Meta:
        """."""

        model = Post
        exclude = ("id",)
