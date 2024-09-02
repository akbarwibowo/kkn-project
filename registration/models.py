from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserExtend(models.Model):
    user_type_choices = {
        "super_user": "super_user",
        "special_user": "special_user",
        "user": "user",
        "visitor": "visitor"
    }
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    rt = models.IntegerField(max_length=3)
    rw = models.IntegerField(max_length=3)
    user_type = models.CharField(max_length=20, choices=user_type_choices, default=user_type_choices['user'])
