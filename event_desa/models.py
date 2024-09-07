from django.db import models
from registration.models import UserExtend

# Create your models here.


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    event_target = models.CharField(max_length=50)
    edited = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    user = models.ForeignKey(UserExtend, on_delete=models.CASCADE)


class EventMessage(models.Model):
    type_choices = {
        'rejected': 'rejected',
        'revision': 'revision',
    }

    type = models.CharField(max_length=8, choices=type_choices)
    message = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
