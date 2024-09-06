from django.db import models
from registration.models import UserExtend

# Create your models here.


class Information(models.Model):
    info_name = models.CharField(max_length=100)
    info_description = models.TextField()
    info_created_date = models.DateField()
    info_image = models.BinaryField(null=True)
    edited = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    user = models.ForeignKey(UserExtend, on_delete=models.CASCADE)


class InformationMessage(models.Model):
    type_choices = {
        'rejected': 'rejected',
        'revision': 'revision',
    }

    type = models.CharField(max_length=8, choices=type_choices)
    message = models.TextField()
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
