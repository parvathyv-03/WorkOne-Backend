from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('hr','HR'),
        ('employee','Employee')
    )

    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15,blank=True,null=True)

    def __str__(self):
        return self.username