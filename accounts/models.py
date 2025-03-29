from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


class CustomUser(AbstractUser):
    username = CharField(max_length=150, unique=True)
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def get_username(self):
        return self.username
