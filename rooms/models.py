from django.db import models
from django.conf import settings
from common.models import CommonModel


class Room(CommonModel):
    """Room Model Definition"""

    class KindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=50, default="대한민국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=KindChoices.choices)

    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # manytomany라는 새로운 유형을 배웠습니다
    amenities = models.ManyToManyField("rooms.Amenity")

    def __str__(self):
        return self.name


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    # 복수형을 바꿔봅시다.
    class Meta:
        verbose_name_plural = "Amenities"
