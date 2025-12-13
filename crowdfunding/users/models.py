from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bluecard = models.BooleanField(default=False)
    def __str__(self):
        # __str__ method to return the username of the user
        return self.username 