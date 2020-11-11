from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User


class LikeDislike(models.Model):
    """model of Like"""

    LIKE = 1
    DISLIKE = -1

    VOTES = ((DISLIKE, "Dislike"), (LIKE, "Like"))

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("post",)},
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Reaction user {self.user} to {self.content_object}"
