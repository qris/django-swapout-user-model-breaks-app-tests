from django.db import models
from django.db.models import fields
from django.contrib.auth.models import AbstractUser, UserManager

class IntranetUser(AbstractUser):
    objects = UserManager()
    title = fields.CharField(max_length=100)
