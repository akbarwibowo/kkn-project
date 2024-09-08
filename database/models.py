import datetime

from django.db import models
from registration.models import User

# Create your models here.


class Batch(models.Model):
    input_person = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today())


class Resident(models.Model):
    gender_choice = {
        'male': 'male',
        'female': 'female'
    }
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=gender_choice)
    pregnant = models.BooleanField(default=False)
    birth_date = models.DateField()
    work = models.CharField(max_length=10, default='unemployed')
    rt = models.SmallIntegerField()
    rw = models.SmallIntegerField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


class BatchMessage(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    message = models.TextField()
