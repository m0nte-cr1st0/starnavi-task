from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended basic User model"""

    last_request = models.DateTimeField(blank=True, null=True)
