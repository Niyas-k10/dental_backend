from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)   
    phone = models.CharField(max_length=15, unique=True)  

    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    sex = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username