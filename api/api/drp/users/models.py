from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # TODO: make email field unique (and nullable to keep it optional).

    # TODO: normalize phone number
    phone = models.CharField(
        "phone number", max_length=17, blank=True, unique=True, null=True
    )

    class Meta:
        swappable = "AUTH_USER_MODEL"
