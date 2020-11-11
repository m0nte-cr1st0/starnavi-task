from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import serializers

from communication.models import LikeDislike


class LikeDislikeSerializer(serializers.ModelSerializer):
    """Like/dislike serializer"""

    content_type = serializers.CharField(source="content_type.model")

    class Meta:
        """."""

        model = LikeDislike
        exclude = ("id", "user")

    def create(self, validated_data: dict) -> Meta.model:
        """
        Add user from request to validate data.
        Set (or change) like/dislike.
        User can't to vote twice.
        """
        try:
            content_type = ContentType.objects.get(
                model=validated_data["content_type"]["model"]
            )
            validated_data["content_type"] = content_type
        except (MultipleObjectsReturned, ContentType.DoesNotExist) as error:
            raise serializers.ValidationError("Wrong content_type") from error
        validated_data["user"] = self.context["request"].user
        if (
            obj_qs := self.Meta.model.objects.filter(
                content_type=content_type, user=self.context["request"].user
            )
        ) :
            obj = obj_qs.first()
            if validated_data["vote"] == obj.vote:
                raise serializers.ValidationError("Can't be vote twice")
            obj.vote = validated_data["vote"]
            obj.save(update_fields=("vote",))
        else:
            obj = self.Meta.model.objects.create(**validated_data)
        return obj


class ActivitySerializer(serializers.Serializer):
    """Likes statistic serializer"""

    likes_count = serializers.IntegerField()
    date = serializers.DateTimeField(format="%Y-%m-%d")
