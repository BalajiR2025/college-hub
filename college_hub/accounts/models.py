from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    department = models.CharField(max_length=50)
    year = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)