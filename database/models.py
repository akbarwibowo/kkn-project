from django.db import models
from registration.models import UserExtend

# Create your models here.


class Batch(models.Model):
    input_person = models.ForeignKey(UserExtend, on_delete=models.CASCADE)


class Resident(models.Model):
    gender_choice = {
        'male': 'male',
        'female': 'female'
    }
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=gender_choice)
    pregnant = models.BooleanField(default=False)
    birth_date = models.DateField()
    work = models.BooleanField(default=False)
    rt = models.SmallIntegerField()
    rw = models.SmallIntegerField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
