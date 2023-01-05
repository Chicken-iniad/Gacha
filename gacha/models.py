from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Monster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    monsters = models.TextField(null=True, blank=True)