from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Monster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monsters = ArrayField(models.CharField(max_length=100))