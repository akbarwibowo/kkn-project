from django.db import models
from registration.models import UserExtend

# Create your models here.


class Information(models.Model):
    info_name = models.CharField(max_length=100)
    info_description = models.TextField()
    info_created_date = models.DateField()
    info_image = models.ImageField()
    edited = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    user = models.ForeignKey(UserExtend, on_delete=models.CASCADE)
