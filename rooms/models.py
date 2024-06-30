from django.db import models
from django.conf import settings
from common.models import CommonModel
from django.db.models import Avg
from django.core.validators import MinValueValidator


class Room(CommonModel):
    """Room Model Definition"""

    class KindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=50, default="대한민국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    rooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    toilets = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=KindChoices.choices)

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    # manytomany라는 새로운 유형을 배웠습니다
    amenities = models.ManyToManyField(
        to="rooms.Amenity",
        related_name="rooms",
    )

    category = models.ForeignKey(
        to="categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    # ORM을 나중에 API로 쓰고 싶으면, 모델의 method로 정의한다.
    def total_amenities_model(self):
        return self.amenities.count()

    def rating(self):
        average_rating = self.reviews.all().aggregate(Avg("rating"))["rating__avg"]
        if average_rating is None:
            return "No Reviews"
        else:
            return round(average_rating, 2)


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    # 복수형을 바꿔봅시다.
    class Meta:
        verbose_name_plural = "Amenities"
