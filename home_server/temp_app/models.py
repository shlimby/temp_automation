from django.db import models
from datetime import datetime

from django.db.models.fields import CharField


# Create your models here.
class ChatUser(models.Model):
    """Model for User
    """
    username = models.CharField(max_length=50, unique=True)
    bot_token = models.CharField(max_length=100, blank=True, null=True)
    chat_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username


class Place(models.Model):
    """Model for Places"""
    owner = models.ManyToManyField(ChatUser)
    zip_code = models.CharField(max_length=10)
    country_code = models.CharField(max_length=4)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return "{}".format(self.name)


class Room(models.Model):
    """Model for rooms in every Place"""
    room_type_choices = [
        (1, 'Schlafzimmer'),
        (2, 'Wohn- und Arbeitszimmer'),
        (3, 'Kinderzimmer'),
        (4, 'Küche'),
        (5, 'Badezimmer'),
        (6, 'Keller'),
    ]
    room_type = models.IntegerField(choices=room_type_choices, default=1)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}, {}".format(self.name, self.place)


class Sensor(models.Model):
    """ Model for Place of Sensor
    """
    name = models.CharField(max_length=50, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()

    def __str__(self) -> str:
        return "{}, {}".format(self.name, self.room)


class OutsideEntrie(models.Model):
    """Model for data ouside """
    timestamp = models.DateTimeField(default=datetime.now)
    temp = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}, {}".format(self.timestamp, self.place)


class Entrie(models.Model):
    """ Model for sensors
    """
    timestamp = models.DateTimeField(
        default=datetime.now, null=True, blank=True)

    ip = models.GenericIPAddressField(null=True, blank=True)
    temp_in_deg = models.FloatField()
    humid_perc = models.FloatField()
    window_open = models.BooleanField(null=True, blank=True)
    # many-to-one relationship
    sensor = models.ForeignKey(
        Sensor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    out_data = models.ForeignKey(
        OutsideEntrie, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return "{}, {}".format(self.timestamp, self.sensor)
