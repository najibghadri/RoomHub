from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError

def room_taken(instance):
    all_events_in_room = Event.objects.filter(room=instance.room)
    for event in all_events_in_room:
        if instance == event:
            continue
        if instance.start <= event.start and instance.end > event.start:
            return True
        if instance.start < event.end and instance.end >= event.end:
            return True
    return False

class CustomUser(AbstractUser):
    email = models.EmailField(
	    verbose_name='email address',
	    max_length=255,
	    unique=True,
        blank=False,
        null=False
        )
     
    def __str__(self):
        return self.username

class Event(models.Model):
    is_public = models.BooleanField(default='True')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    start = models.DateTimeField('Start')
    end = models.DateTimeField('End')
    organizer_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def clean(self):
        if self.start >= self.end:
            raise ValidationError({'start': 'Start date must be earlier than end date'})
        if room_taken(self):
            raise ValidationError({'room': 'This room is reserved during this date time. Try another time or another room!'})
    
class Room(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
