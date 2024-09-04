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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    rt = models.IntegerField()
    rw = models.IntegerField()
    user_type = models.CharField(max_length=20, choices=user_type_choices, default=user_type_choices['user'])
