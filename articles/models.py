from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify

from accounts.models import User
from communication.models import LikeDislike


class Post(models.Model):
    """model of Post"""

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True)
    content = models.TextField()
    votes = GenericRelation(LikeDislike, related_query_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        """Generate slug from title"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
