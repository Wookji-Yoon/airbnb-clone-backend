from django.db import models
from django.conf import settings


class Room(models.Model):
    """Room Model Definition"""

    class KindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    country = models.CharField(max_length=50, default="대한민국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    per_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=KindChoices)

    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Amenity(models.Model):
    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True)
